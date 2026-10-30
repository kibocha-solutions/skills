# Model Selection and Delegation Examples

Read a scenario relevant to the current assignment before dispatch. These scenarios illustrate principles and do not limit their application to the listed work. Select only models and tools actually available and permitted. A stronger model can coordinate or resolve hard decisions; the model used for each bounded execution or inspection task depends on that task's own requirements.

## 1. Inspect one screen

**Situation:** Confirm whether a specific candidate page shows an AI score exactly once.

**Assignment:** Tell an inspector the account role, record state, page, navigation steps, expected score placement, and evidence to capture. Ask for yes, no, or blocked with a screenshot and observed details. A suitable lighter model such as Luna or Haiku performs the check. The coordinator decides whether the evidence satisfies the requirement.

**Escalate:** Use stronger judgment if the expected behavior itself is ambiguous or independent interpretation of conflicting requirements is required. Do not ask the inspector to guess which rule governs.

## 2. Fix a known frontend defect

**Situation:** An inspector has shown that an empty version appears in a list. The coordinator has identified the intended behavior and the affected component.

**Assignment:** Give a lighter executor the file, the precise condition for hiding the entry, the behavior to preserve, and a focused verification request. Assign a separate inspector to recheck the page.

**Escalate:** Route an unresolved architecture or product decision to a stronger model when the coordinator cannot resolve it. Writing code alone is not a reason to select the stronger model.

## 3. Implement a backend change with settled semantics

**Situation:** The coordinator has determined the exact scorecard rejection outcome and affected endpoint.

**Assignment:** Give a lighter executor the endpoint, accepted state transition, expected response, authorization boundary, and relevant files. Require the executor to report its changes and verification. A different inspector verifies the result.

**Escalate:** Use stronger reasoning if conflicting domain rules or transactional behavior remain unresolved. Once settled, return the bounded implementation to a suitable lighter executor.

## 4. Separate design from migration execution

**Situation:** A schema change is needed, but data ownership and backwards compatibility are not settled.

**Assignment:** Have the coordinator or a suitable stronger reasoning specialist resolve the schema, preservation and rollback boundaries, and authorization. Give a lighter executor the approved migration specification and exact target. Do not run a shared database migration without the required authorization and maintenance boundary.

**Escalate:** Keep the design with the stronger role while risk or semantics remain uncertain. Do not assign an entire mixed batch to a stronger executor merely because it contains a migration.

## 5. Split a large audit matrix

**Situation:** A brief has many partial and missing items across several domains.

**Assignment:** The coordinator records the complete scope and dependencies, then assigns small batches with named outcomes and clear acceptance criteria. A lighter inspector gathers evidence for exact checks. A lighter executor implements a specified fix. Use a shared environment and coordinate a consolidated rebuild when authorized.

**Escalate:** Assign a stronger reasoning task only for an unresolved design question or difficult diagnosis. Do not label fourteen heterogeneous items as one simple assignment or use the number of items alone to select a stronger executor.

## 6. Resolve ambiguous requirements

**Situation:** Two controlling documents appear to disagree about whether a rejected scorecard can be edited.

**Assignment:** The coordinator compares authority, context, and available decisions. If necessary, use a stronger reasoning specialist for a bounded comparison with citations. The coordinator resolves the conflict or asks the user when authority or intent cannot be determined.

**Follow through:** Give the accepted decision to a lighter executor as concrete state rules, and assign an independent inspector to verify them.

## 7. Inspect a reported sorting issue

**Situation:** A table's sort indicator changes, but the row order may not.

**Assignment:** Ask a lighter inspector to record the initial order, exact column and clicks, resulting order, viewport, and evidence. Report actual observations, including no change or an inaccessible page. The coordinator evaluates the observations.

**Escalate:** Use stronger reasoning to investigate only if the concrete evidence leaves a nontrivial runtime or comparator cause unresolved. An inspector records what it can observe; it does not invent a product decision.

## 8. Apply an exact sorting fix

**Situation:** The coordinator has traced the defect and specified the correct field and comparator behavior.

**Assignment:** Assign a lighter executor the exact files, expected ordering including nulls and ties, and the boundaries of the change. Preserve unrelated work. After the authorized refresh, have the original inspector repeat the same browser check.

**Escalate:** A stronger diagnostic worker may investigate conflicting runtime evidence or an unclear data contract. Report the reason and split out the later implementation.

## 9. Diagnose conflicting evidence

**Situation:** A source change appears correct, but the live page still behaves as before and runtime ownership is unclear.

**Assignment:** First give a lighter worker a finite evidence collection checklist: served version, process or container identity, source revision, and observed endpoint. If the results conflict in a way that needs interpretation, route the diagnosis to a stronger model or coordinator with the collected evidence.

**Follow through:** Once the cause is known, give the appropriate worker a bounded action. Do not restart shared services without the applicable authorization.

## 10. Implement a small documentation change

**Situation:** A user has approved an exact wording correction and identified the document.

**Assignment:** Have a lighter executor apply the correction without changing other claims, then have a separate inspector compare the rendered or source result against the specified wording as appropriate.

**Escalate:** Use a stronger specialist for unresolved legal meaning, conflicting authorities, or a complex editorial decision. Do not infer that all documentation work is routine.

## 11. Handle a user correction during work

**Situation:** An executor was launched on a stronger model for a batch that contains separable routine fixes. The user directs the coordinator to use a lighter model for clear tasks.

**Assignment:** Acknowledge the correction. Determine the worker's safe stopping point and preserve its partial work. Use supported controls to redirect or reassign the remaining bounded routine work to a suitable lighter model. Keep any genuinely unresolved design question separately assigned and explain any platform limitation.

**Avoid:** Continuing the entire batch on the stronger model simply because it has already started. Do not claim that an existing chat changed models unless the platform confirms it.

## 12. Model selection unavailable

**Situation:** The platform can create a worker, but its creation tool does not expose a model selector.

**Assignment:** Record that selection is unavailable, use an authorized available worker if appropriate, and make the limitation clear to the coordinator and user when material. Do not present a requested model as active without confirmation.

**Escalate:** If the requested work cannot be performed reliably with available capabilities, report the blocker and preserve progress.

## 13. Credentials or user action needed

**Situation:** A browser inspector reaches a sign-in screen and has no authorized credentials.

**Assignment:** The inspector reports the blocker to its parent with the account role and required action. The coordinator uses the approved secure path to request user action. Resume the bounded check once access is available.

**Avoid:** Putting passwords in assignments or worker messages, inventing access, or requiring the user to operate a proposal card when the platform permits the coordinator to dispatch the already-authorized work.

## 14. Confirm task completion

**Situation:** Executors report fixes and inspectors return observations against the brief.

**Assignment:** Have a suitable lighter inspector check each specified acceptance item and send evidence to its parent. The coordinator compares evidence with the complete scope, resolves discrepancies, and reports any remaining blocker. Mark the task complete only after the requested acceptance evidence exists.

**Escalate:** Use stronger reasoning where evidence or requirements genuinely conflict. Do not treat a worker's assertion, a focused test, or a progress percentage as proof of the full outcome.
