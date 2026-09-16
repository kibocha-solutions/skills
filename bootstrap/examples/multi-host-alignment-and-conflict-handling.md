# Bootstrap Examples: Multi-Host Alignment and Conflict Handling

## 1. Instruction File Alignment

### Bad (Overwriting Unrelated Settings or Using Symlinks)

```bash
# BAD: Overwriting the user's entire CLAUDE.md and deleting custom instructions
cat AGENTS.md > ~/.claude/CLAUDE.md

# BAD: Symlinking instructions to repository path
ln -s /mnt/data/workspace/skills/AGENTS.md ~/.codex/AGENTS.md
```

Defects:
- Completely erases custom project instructions outside the shared block.
- Symlinks break when working across container boundaries or different mount points.

### Good (Non-Destructive Marker Block Embedding)

```markdown
<!-- BEFORE ALIGNMENT in ~/.claude/CLAUDE.md -->
# User Local Preferences
Always use 2 spaces for JSON indentation.

<!-- BEGIN SHARED SKILLS RULES -->
(Old shared rules content...)
<!-- END SHARED SKILLS RULES -->

# User Tool Preferences
Prefer python3 over python.
```

When `align_agent_rules` runs:
- Content outside `BEGIN SHARED SKILLS RULES` and `END SHARED SKILLS RULES` is preserved untouched.
- Shared rules are atomically updated between the markers.
- Legacy `@skills/AGENTS.md` pointer lines are safely removed.
- Redundant `~/.claude/AGENTS.md` is removed to avoid duplicate host instruction files.
