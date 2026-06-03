# Project-References Master Index

This directory contains comprehensive instructions for all AI coding assistants working on Vibe Code Canon projects.

## Structure

```
00-project-references/
├── README.md (this file)
├── 00-core-canons/                     # Universal writing and formatting rules
├── 01-technical-documentation/         # Documentation canons and standards
├── 02-security/                        # Security standards
├── 03-ci-cd/                           # Git, commits, pipelines
├── 04-testing/                         # Testing procedures
├── 05-programming-standards/           # Code standards
├── 06-deployment/                      # Infrastructure, deployment
└── 07-project-wide-instructions/       # Agent instructions (AGENTS.md, Copilot, Cursor)
    ├── AGENTS.md                       # Universal instructions (all agents)
    ├── github-copilot/                 # GitHub Copilot specific
    └── cursor/                         # Cursor AI specific
```

## Agent Instructions Files

All three files (`AGENTS.md`, Copilot, Cursor) contain **IDENTICAL instructions with ABSOLUTE AUTHORITY**:

1. **Task Clarification Protocol** - MANDATORY before starting work
2. **Context Management** - Load ONLY relevant files (avoid overwhelm)
3. **Core Canon** - MUST read `00-core-canons/_core_canon.md` first
4. **Security Checklist** - NON-NEGOTIABLE before every commit
5. **Formatting Rules** - No emojis, no emdashes, kebab-case naming
6. **Conventional Commits** - Standard commit message format
7. **.gitignore Management** - Active verification of staging area
8. **Anti-Patterns** - No summary documents, no temp file litter

## Reference Domains

Each reference directory contains deep-dive canonical instructions for specific domains:

### 00-core-canons/
**Use when:** ALWAYS - read `_core_canon.md` FIRST before any task  
**Contains:** Universal writing rules, formatting absolutes, voice guidelines, quality assurance checklist

### 01-technical-documentation/
**Use when:** Creating or updating any technical documentation  
**Contains:** Documentation canons for all types (API, architecture, etc.)

### 02-security/
**Use when:** Authentication, encryption, sensitive data handling  
**Contains:** Security standards, OWASP prevention, secure coding

### 03-ci-cd/
**Use when:** Git commits, pipeline setup, deployment automation  
**Contains:** Git workflows, Conventional Commits, pipeline configs

### 04-testing/
**Use when:** Writing tests (unit, integration, E2E, performance)  
**Contains:** Testing strategies, standards, test data management

### 05-programming-standards/
**Use when:** Writing application code in any language  
**Contains:** Language-specific standards, design principles, error handling

### 06-deployment/
**Use when:** Infrastructure setup, Kubernetes, deployment procedures  
**Contains:** Deployment patterns, IaC standards, monitoring

## Installation

Run these commands from your project root directory:

### For GitHub Copilot
```bash
cp -r 07-project-wide-instructions/github-copilot/.github ./
```

### For Cursor AI
```bash
cp -r 07-project-wide-instructions/cursor/.cursor ./
cp 07-project-wide-instructions/AGENTS.md ./
```

### For Google Antigravity (or other agents)
```bash
cp 07-project-wide-instructions/AGENTS.md ./
```

## Critical Principles

1. **Absolute Authority** - These instructions MUST be followed at all times
2. **Context Management** - Load ONLY relevant files for current task
3. **Read Core Canon First** - MANDATORY before any work
4. **Task Clarification** - MUST confirm understanding before proceeding
5. **Security First** - NON-NEGOTIABLE checklist before every commit
6. **No Assumptions** - Read existing code explicitly before referencing

---

**Version:** 1.0 (December 29, 2025)
