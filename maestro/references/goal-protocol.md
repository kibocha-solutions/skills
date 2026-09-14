# Goal Protocol

## Create `goal.md`

Create `goal.md` only when the user requests a tracked goal or the governing runtime requires it.

```yaml
objective: "<user-visible outcome>"
success_criteria:
  - id: SC-1
    description: "<falsifiable result>"
    verification: "<exact check>"
thresholds:
  progress:
    stall_turns: 4
  quality:
    max_retries: 2
  scope:
    max_added_tasks_pct: 30
```

## Check progress

1. Count continuations since the last task became `[x]`.
2. Compare the count with `stall_turns`.
3. Re-read the plan and active task when the threshold is reached.
4. Split the stalled task into smaller tasks.
5. Record the split in `tasks.md` and `walkthrough.md`.
6. Continue with the first new task.

## Check quality

1. Count retries of the same logical task.
2. Track failed checks after a task was marked `[x]`.
3. Reopen the failed task when the threshold is reached.
4. Record the failure pattern and corrected approach.
5. Revise the affected plan section.
6. Run the revised verification path.

## Check scope

1. Count original tasks.
2. Count tasks under `## Added`.
3. Calculate the added-task percentage.
4. Stop when the approved threshold is reached.
5. Report the original count, added count, percentage, and added scope.
6. Ask the user whether to accept, trim, or separate the added work.
7. Continue only after the user decides.

## Update the goal

1. Change the objective or success criteria only after the user changes the scope or outcome.
2. Add a dated change-log entry.
3. Update the plan and tasks to match.
4. Do not lower a success criterion to make failed work pass.
