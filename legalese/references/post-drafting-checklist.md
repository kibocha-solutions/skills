# Post-Drafting Checklist

Mandatory final-pass verification executed after drafting and before delivery. The agent runs this checklist silently. On an audit request from the user, reproduce the completed checklist with pass/fail status and evidence for each item.

## Contents

- [1. Authority Register Compliance](#1-authority-register-compliance)
- [2. Synonym Stacking Audit](#2-synonym-stacking-audit)
- [3. Termination Phrase Distribution](#3-termination-phrase-distribution)
- [4. Architectural Fission](#4-architectural-fission)
- [5. Reversibility of Advantage](#5-reversibility-of-advantage)
- [6. Supremacy Calibration](#6-supremacy-calibration)
- [7. Closed Ecosystem](#7-closed-ecosystem)
- [8. Severability Tier Match](#8-severability-tier-match)
- [9. Adversarial Reading](#9-adversarial-reading)
- [10. Structural Fidelity](#10-structural-fidelity)
- [11. Sovereign Economy](#11-sovereign-economy)
- [12. Register Coherence](#12-register-coherence)

---

## 1. Authority Register Compliance

**Check:** The `AUTHORITY_REGISTER` flag (declared in `SKILL.md`) was set before drafting. The output vocabulary, sentence structure, Latin usage, and termination phrases fall within the active tier's boundaries as defined in `references/register-guide.md`.

**Pass criteria:**
- The flag was set at CoLT Step 1.
- No word or construction from a higher tier's "in bounds" list appears unless it is also in bounds at the active tier.
- No word or construction from the active tier's "out of bounds" list appears.

**Common failures:**
- Sovereign vocabulary leaking into a Standard or Formal draft (e.g., "notwithstanding" in a privacy policy).
- Standard simplicity leaking into a Sovereign or Archaic draft (e.g., "will not apply" where "shall not stand" is the tier target).

---

## 2. Synonym Stacking Audit

**Check:** No enumerated chain contains two or more words that share the same legal vector (Doctrine 2).

**Pass criteria:**
- For every word in every enumerated chain, an independent legal vector can be stated.
- No two words in the same chain share a vector.

**Common failures:**
- "cancel, nullify, invalidate, and void" — four words, one vector (termination of legal force).
- "rights, entitlements, and privileges" — three words that often share the same vector unless the context establishes distinct legal domains for each.

**Tier note:** This check is universal across all tiers.

---

## 3. Termination Phrase Distribution

**Check:** No closing phrase of finality appears more than once within the instrument (Doctrine 2, distribution rule).

**Pass criteria:**
- Each termination phrase from `assets/termination-phrases.md` (or its modern equivalent at Standard/Formal) appears at most once.
- The phrase deployed at each clause is the one whose legal character best matches that clause's function.

**Common failures:**
- "void ab initio" used in both the repugnancy clause and the severability clause.
- A modern equivalent like "has no legal effect" repeated across three separate provisions.

---

## 4. Architectural Fission

**Check:** No clause carries more than one primary command — one trigger, one prohibition, or one consequence (Doctrine 3).

**Pass criteria:**
- The fission decision test passes for every clause: removing one part of the sentence does not leave a complete, operative standalone command.
- Parent clauses introduce governing conditions; child paragraphs carry individual consequences or exceptions.

**Common failures:**
- A single clause that both prohibits an action and specifies the penalty for violation — these are two separate commands.
- A grant clause that also contains a limitation on the grant — the grant and the limitation are separate commands.

**Tier note:** This check is universal. At Archaic, sentence structure may be ornate and deeply nested, but each clause must still carry a single primary command.

---

## 5. Reversibility of Advantage

**Check:** No phrasing implies the instrument or sovereign is requesting, hoping, or collaborating rather than granting or commanding (Doctrine 4, adjusted for tier).

**Pass criteria by tier:**
- **Standard:** The instrument grants and explains. No begging or hedging, but the tone is collaborative. "You have the right to..." is acceptable. "We kindly ask that you..." is a failure.
- **Formal:** The instrument binds through contractual mechanics. "The Party shall..." is acceptable. "The Party is encouraged to..." is a failure unless framed as a non-binding recommendation.
- **Sovereign:** Power flows downward. The instrument commands and grants. "This right is hereby vested in..." is the pattern. "It is hoped that..." is a critical failure.
- **Archaic:** Maximum sovereign command. The instrument decrees. Any construction that positions the subject as doing the instrument a favour is a failure.

**Common failures:**
- "We hope the parties will comply with..." (begging at any tier).
- "The user is encouraged to review..." (hedging where a Standard-tier "Review the terms before..." would be direct).

---

## 6. Supremacy Calibration

**Check:** Supremacy mechanics match the instrument's rank — Supreme, Master, or Subordinate (Doctrine 5).

**Pass criteria:**
- Supreme instruments assert global preclusion.
- Master instruments assert domain-specific supremacy.
- Subordinate instruments acknowledge their superior instrument cleanly.
- The instrument's rank was stated or inferred and confirmed before drafting.

**Tier note:** The *mechanics* of supremacy are universal, but the *expression* is tier-gated. At Standard, supremacy is a plain statement ("This Agreement takes priority over..."). At Sovereign, it is a notwithstanding frame. See `references/register-guide.md`.

---

## 7. Closed Ecosystem

**Check:** All cross-references are exact. No term defined elsewhere in the instrument is redefined, summarised, or paraphrased (Doctrine 6).

**Pass criteria:**
- Every reference to a concept, prohibition, or penalty established elsewhere uses the exact defined term and section reference.
- No "soft" paraphrase of a defined term appears anywhere in the instrument.

**Common failures:**
- Section 8 refers to "the prohibited outcomes" when Section 3 defines them as "Intolerable Outcomes" — a paraphrase that creates ambiguity.
- A severability clause that restates the definition of "void" differently from the repugnancy clause.

**Tier note:** Universal across all tiers.

---

## 8. Severability Tier Match

**Check:** The severability model matches the active tier (Doctrine 7).

**Pass criteria:**
- **Standard / Formal:** Standard severability — invalid provisions are severed, remaining provisions survive.
- **Sovereign / Archaic:** Elite severability — invalid provisions are severed, but if severance frustrates the essential sovereign intent, the entire instrument perishes.

**Common failures:**
- A Sovereign-tier constitution using standard severability ("the rest remains in effect") without the sovereign-core protection clause.
- A Standard-tier service agreement using elite severability ("the entire agreement shall perish") — disproportionate for a commercial instrument.

---

## 9. Adversarial Reading

**Check:** At least one adversarial reading was tested against the drafted text. No open loopholes remain (Doctrine 8).

**Pass criteria:**
- For each substantive clause, at least one motivated adversarial interpretation was identified and tested.
- The drafted language forecloses that interpretation, or the loophole was flagged to the user.

**Common failures:**
- A prohibition that says "shall not do X" but does not address attempts to achieve the same outcome through an intermediary.
- A grant of rights that does not specify whether the right is exclusive or non-exclusive.

**Tier note:** Universal. The sophistication of the adversarial reading should match the tier — a Standard-tier privacy policy faces different attack vectors than a Sovereign-tier constitution.

---

## 10. Structural Fidelity

**Check:** When editing existing text, the structural hierarchy matches the user's source (Doctrine 9). No numbering, lettering, indentation, or heading was manufactured, removed, or altered without explicit permission.

**Pass criteria:**
- The output's enumeration hierarchy is identical to the input's.
- Any structural change was requested by the user or approved after an advisory override.

**Tier note:** Universal across all tiers.

---

## 11. Sovereign Economy

**Check:** No redundant flourish remains that does not close a loophole, establish authority, or carry an independent legal vector.

**Pass criteria:**
- Every classical construction (at Sovereign/Archaic) carries legal load, not decoration.
- Every adjective and adverb earns its place by narrowing scope, adding a distinct vector, or closing a specific loophole.
- At Standard/Formal, plain-language concision: no sentence survives only because it sounds polished.

**Common failures:**
- "absolutely, completely, and utterly void" — three adverbs, one vector (totality). Use one or none.
- "This supreme, inviolable, and sacred right" — "supreme" and "inviolable" may carry distinct vectors (rank vs. protection from interference), but "sacred" adds no legal vector. Remove it.
- "The parties hereto mutually agree and covenant between themselves that..." — "mutually," "between themselves," and "hereto" are all doing the same work as "the parties agree."

**Tier note:** Economy applies at every tier, but its expression differs. At Standard, economy is brevity. At Archaic, economy is density — every word in an ornate construction must carry independent weight.

---

## 12. Register Coherence

**Check:** The output reads naturally within the target register. No jarring register shifts occur within the same section.

**Pass criteria:**
- A reader familiar with the target register would recognise the output as native to that register.
- No sentence is over-elevated for its tier (Sovereign vocabulary in a Standard draft).
- No sentence is under-elevated for its tier (casual phrasing in a Sovereign draft).
- Where mixed registers are used within a document (e.g., Archaic preamble, Formal schedules), the transitions are deliberate and the tier shift is noted.

**Common failures:**
- A Formal contract that suddenly uses "shall perish" in one clause and "will not apply" everywhere else.
- A Sovereign constitution that uses "is canceled" in a single provision amid otherwise classical language.
