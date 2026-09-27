# Issue Standards

Standards for authoring bug reports, feature requests, and issue descriptions across repositories, synthesized from Microsoft and Google open-source engineering practices.

## Core principles

1. File a single issue per problem or feature request. Never combine multiple bugs or requests in one issue.
2. Search existing open and closed issues before filing to prevent duplicate tickets.
3. Write for a new reader. State the problem clearly and objectively so any maintainer or contributor can reproduce and resolve it without prior session context.
4. Never include personal or sensitive identifying information. This covers registration, certificate, tax, and national ID or passport numbers, bank particulars, phone numbers, personal email addresses, and private individuals' names, unless expressly authorized by the user.
5. Apply the absolute AI-attribution prohibition. Never attribute an issue or its contents to AI, a model, an agent, or automated tools.
6. Keep internal agent plans, sessions, memory files, and hidden prompt instructions out of issues.

## Bug report structure

### 1. Title
Write a concise, descriptive summary of the specific failure mode.
1. Use imperative or clear defect phrasing, such as `Export fails with timeout on datasets over 10k rows`.
2. Do not use vague titles such as `Broken export` or `Bug in system`.

### 2. Environment
State the exact execution context:
1. Software or package version.
2. Operating system and architecture.
3. Runtime version, such as Node.js, Python, or Java.
4. Relevant browser, client, or database versions.
5. Active plugins, flags, or configuration profiles.

### 3. Problem description
1. State what happened clearly.
2. State what was expected to happen.
3. Isolate the defect from third-party tools or external interference.

### 4. Steps to reproduce
Provide numbered, deterministic steps from a clean state:
1. Initial condition or setup
2. Exact command, action, or API call
3. Observed result

### 5. Minimal reproducible example
1. Provide the smallest self-contained code snippet, configuration, or test case that reproduces the issue.
2. Provide code as copyable text in code fences, never as an image or screenshot.
3. Provide a minimal reproduction repository link when the bug requires multi-file context.

### 6. Logs, traces, and visual evidence
1. Include exact console errors, stack traces, and exit codes in code fences.
2. Sanitize logs to ensure no credentials, tokens, internal URLs, or sensitive identifiers are present.
3. Use screenshots or recordings to illustrate user interface defects; do not substitute images for text reproduction steps.

## Feature request structure

### 1. Title
State the proposed capability directly, such as `Add OIDC support for GitLab pipeline triggers`.

### 2. Problem or use case
Explain the concrete scenario or friction that motivates the request. Describe the user-visible or operator-visible outcome.

### 3. Proposed solution
Describe the desired behavior, API shape, or configuration interface. Mention any evaluated alternatives and why the proposed approach is preferred.

### 4. Non-goals and boundaries
State what the proposed change explicitly does not attempt to cover.

## Examples

Inspect [issue examples](../examples/issue-examples.md) for contrasting good versus bad bug reports and feature requests.

## Quality checklist

- [ ] Existing issues searched for duplicates before opening.
- [ ] Single issue covers exactly one problem or feature request.
- [ ] Title describes the specific defect or capability clearly.
- [ ] Environment details, including software version, operating system, and runtime, are complete.
- [ ] Reproduction steps are numbered, sequential, and deterministic.
- [ ] Code samples and stack traces are formatted in code fences as copyable text.
- [ ] No personal or sensitive identifying information appears without express authorization.
- [ ] No agent session notes, internal paths, or AI attribution appear.
