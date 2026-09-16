---
name: skill-creator
description: Create, revise, evaluate, benchmark, package, and optimize Codex skills. Use for new skills, skill updates, SKILL.md restructuring, trigger-description optimization, skill test cases, baseline comparisons, and skill-quality measurement.
---

# Skill Creator

## 1. Establish the task

1. Read `references/skill-authoring-standard.md` before creating or revising a
   skill or `AGENTS.md`.
2. Classify the request as creation, revision, evaluation, description
   optimization, or packaging.
3. Extract existing requirements from the conversation and supplied files.
4. Confirm only missing requirements that materially change the result:
   - skill responsibility
   - trigger conditions
   - required inputs
   - required outputs
   - objective verification
5. Preserve the existing directory name and frontmatter `name` during a
   revision.

## 2. Inspect the skill

1. Read the existing `SKILL.md` from start to finish.
2. Inventory `references/`, `assets/`, `scripts/`, `agents/`, and
   `evals/`.
3. Read each resource required for the requested change.
4. Check available tools and dependencies.
5. Record the current behavior that must remain.
6. Snapshot an existing skill before revision:

```bash
cp -r <skill-path> <skill-workspace>/skill-snapshot/
```

## 3. Write the skill

1. Create this minimum structure:

```text
<skill-name>/
└── SKILL.md
```

2. Add optional resources only when required:

```text
<skill-name>/
├── SKILL.md
├── references/
├── assets/
├── scripts/
└── evals/
```

3. Write YAML frontmatter with:
   - `name`: the directory name
   - `description`: the capability and every trigger condition
   - `compatibility`: required tools or dependencies, only when applicable
4. Put task steps in the body.
5. Use imperative sentences and execution order.
6. Put variant procedures and specifications in `references/`.
7. Put templates and reusable output shells in `assets/`.
8. Put deterministic repeated operations in `scripts/`.
9. Link each resource from the step that requires it.
10. Keep `SKILL.md` below 500 lines.
11. Add a table of contents to any reference longer than 300 lines.
12. Run the checks in `references/skill-authoring-standard.md`.

## 4. Create evaluation cases

1. Create two or three realistic prompts for the skill's main behavior and
   edge cases.
2. Obtain user review when the evaluation scope is subjective or disputed.
3. Save the cases to `evals/evals.json`.
4. Follow `references/schemas.md`.
5. Include `skill_name`, `id`, `prompt`, `expected_output`, and
   `files`.
6. Add objective assertions after the runs start.
7. Leave subjective qualities for human review.

## 5. Prepare the evaluation workspace

1. Create a sibling workspace named `<skill-name>-workspace/`.
2. Create one directory per iteration.
3. Create one descriptively named directory per evaluation case.
4. Write `eval_metadata.json` for each case.
5. Use this structure:

```text
<skill-name>-workspace/
├── skill-snapshot/
└── iteration-1/
    └── <eval-name>/
        ├── eval_metadata.json
        ├── with_skill/
        └── old_skill/
```

6. Use `without_skill/` instead of `old_skill/` for a new skill.

## 6. Run paired evaluations

1. Start the with-skill and baseline run for every case in the same turn when
   independent agents are available.
2. Give each run:
   - the exact prompt
   - the skill path or baseline condition
   - the input-file paths
   - the output directory
   - the required deliverables
3. Use the original snapshot as the baseline for revisions.
4. Use no skill as the baseline for new skills.
5. Draft assertions while runs execute.
6. Save each run's completion metrics immediately to `timing.json`:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

7. Run each case sequentially and omit baseline comparison when independent
   agents are unavailable.

## 7. Grade and aggregate

1. Read `agents/grader.md` before assigning a grader.
2. Use deterministic checks for machine-verifiable assertions.
3. Save each result to `grading.json`.
4. Use the exact grading fields `text`, `passed`, and `evidence`.
5. Aggregate the iteration:

```bash
python -m scripts.aggregate_benchmark \
  <workspace>/iteration-N \
  --skill-name <name>
```

6. Read `agents/analyzer.md` before the analyst pass.
7. Check for:
   - assertions that pass both configurations
   - high-variance cases
   - flaky cases
   - time regressions
   - token regressions
   - capability loss
8. Use `agents/comparator.md` only for a requested blind comparison.

## 8. Present results

1. Generate the review UI with `eval-viewer/generate_review.py`.
2. Include `benchmark.json`.
3. Pass `--previous-workspace` from iteration two onward.
4. Use `--static <output-path>` in a headless environment.
5. Present results directly in chat when no browser or file-presentation tool
   is available.
6. Read `feedback.json` after the user completes the review.
7. Treat empty feedback as acceptance of that case.
8. Stop any viewer process after review.

## 9. Revise and repeat

1. Map each failure or user comment to a general skill defect.
2. Revise the smallest instruction or resource that fixes the defect.
3. Preserve behavior that passed.
4. Run the complete evaluation set in a new iteration.
5. Keep the same baseline unless the comparison question changes.
6. Repeat until:
   - the user accepts the outputs
   - all review feedback is empty
   - further changes produce no material improvement

## 10. Optimize the description

1. Create 20 realistic trigger queries:
   - 8 to 10 positive cases
   - 8 to 10 adjacent negative cases
2. Include formal, casual, abbreviated, typo-bearing, and implicit requests.
3. Avoid trivial positive cases and unrelated negative cases.
4. Save the query set as JSON.
5. Let the user review it with `assets/eval_review.html` when interactive
   review is available.
6. Run:

```bash
python -m scripts.run_loop \
  --eval-set <trigger-eval.json> \
  --skill-path <skill-path> \
  --model <current-model-id> \
  --max-iterations 5 \
  --verbose
```

7. Apply `best_description` only when the held-out score improves.
8. Report the before and after descriptions and scores.
9. Skip optimization when its required CLI is unavailable.

## 11. Package and deliver

1. Run:

```bash
python -m scripts.package_skill <skill-folder>
```

2. Stage manual packages in a temporary directory before copying them to the
   destination.
3. Verify the package exists and contains the final skill.
4. Re-read the final `SKILL.md`.
5. Report the package path, validation results, and any unrun evaluation.

Inspect [evaluation examples](examples/benchmark-and-evaluation-patterns.md) for objective assertion patterns.

## 12. Pre-completion checklist

Before delivering any new or revised skill, confirm evidence exists for each item:

- [ ] Existing `SKILL.md` and related resources read manually in full from start to finish.
- [ ] Frontmatter contains valid `name` and trigger-rich `description`.
- [ ] Body uses imperative sentences organized in execution order.
- [ ] `SKILL.md` body is under 500 lines; deep specs placed in `references/`.
- [ ] Contrasting good vs bad implementations provided in `examples/`.
- [ ] Evaluation cases in `evals/evals.json` are objective and falsifiable.
- [ ] No U+2014 em dashes in normal prose.
- [ ] Zero AI attribution in skill content or metadata.

