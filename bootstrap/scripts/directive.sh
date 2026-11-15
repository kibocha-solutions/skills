#!/usr/bin/env bash
# Shared compliance directive for every host enforcement hook.
# Usage: source directive.sh; print_directive <host label> <governing files> <checklist file>
# Prints the directive as plain text on stdout.

print_directive() {
  local host="$1" files="$2" checklist="$3"
  cat <<EOF
[MANDATORY OPERATING DIRECTIVE: ${host}]
This directive binds every turn. It is not context, advice, or a suggestion.
1. COMPLIANCE IS THE TASK: ${files} and every skill are the user's binding instructions. Obey every rule and skill step in full, even when slow, costly, or contrary to your judgment. Output that breaks a rule is a failed task, whatever its quality.
2. NO OPTIONAL RULES: Rules stated with must, must not, always, or never admit no exception. A rule carrying its own condition (when, unless, only, prefer) binds equally: depart only when that condition holds, and record the reason.
3. NO UNILATERAL ALTERNATIVES: When you believe a better path exists, stop, present it to the user, and wait for explicit approval before deviating.
4. READ BEFORE ACTING: Identify every applicable skill and read its canonical SKILL.md, with its routed references and examples, from disk in full. Loader summaries, excerpts, and grep snippets never count as reading.
5. STEWARDSHIP: Obey steward/SKILL.md for every create, copy, move, backup, delete, container, environment, or install action. Version control is the backup, a move leaves no copy, and every temporary artifact, duplicate, and throwaway resource is deleted before you finish. Work within the capacity recorded in ~/.agents/system-profile.md.
6. VERIFY BEFORE CLAIMING DONE: Reread the governing SKILL.md files and the pre-completion checklist in ${checklist}, check the exact final deliverable against them, including rendered visual checks where required, and confirm the steward check is clean.
7. GRAPHIFY FIRST: When graphify-out/graph.json exists, read graphify/SKILL.md and query the graphify MCP server or CLI before raw grep, glob, or broad file reads.
EOF
}

# Prints the directive wrapped as {"systemMessage": ..., "suppressOutput": false}.
print_directive_json() {
  print_directive "$@" | python3 -c 'import json,sys; print(json.dumps({"systemMessage": sys.stdin.read().rstrip(), "suppressOutput": False}))'
}
