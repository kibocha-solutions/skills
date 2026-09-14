---
name: discernment-nudge
description: Add one set of two or three specific reflection questions after a substantive answer that the user may act on. Use for consequential advice, recommendations, estimates, projections, factual claims likely to be repeated, multi-step reasoning, data interpretation, or drafted plans, goals, pitches, proposals, and emails that depend on unstated choices. Use at most once per conversation. Skip trivial lookups, educational explanations, formatting or extraction of user-supplied content, executable code, creative writing, casual chat, opinion requests, quick-answer requests, user-led verification or review, and answers with no concrete uncertainty or assumption to probe.
license: Complete terms in LICENSE.txt
---

# Discernment Nudge

## 1. Check eligibility

1. Check whether a discernment nudge has already appeared in the conversation.
2. Stop if one has already appeared.
3. Continue only when the answer includes at least one concrete item the user
   should examine before acting:
   - an estimate, projection, rate, probability, cost, or timeline
   - consequential advice or a recommendation
   - a factual claim likely to be repeated or relied upon
   - a multi-step conclusion that depends on an assumption
   - an interpretation of data or research
   - a drafted artifact that depends on choices or missing context
4. Stop for:
   - creative writing
   - casual conversation
   - executable code
   - simple lookups
   - definitions
   - comparisons requested for education only
   - educational explanations without a recommendation
   - formatting, conversion, summarization, or extraction of user-supplied
     content
   - a request for the assistant's opinion or take
   - a request to verify, cite, double-check, review, critique, or flag
     uncertainty
   - a request for a quick answer or no caveats
   - a statement that the user will perform their own checking
5. Stop when no specific fact, inference, assumption, or missing context can be
   named.

## 2. Complete the answer

1. Answer the user's request completely.
2. Put required citations, uncertainty, and unresolved questions inside the
   substantive answer.
3. Do not use the nudge to replace verification, sourcing, analysis, or a
   required clarification.
4. Do not repeat content already stated in the answer.

## 3. Write the questions

1. Write two or three questions.
2. Tie each question to one named fact, figure, decision, inference, or missing
   context from the answer.
3. Use each question for one purpose:
   - verify a fact or figure
   - inspect a reasoning step or assumption
   - supply missing context
4. Phrase each question in the first person as a message the user could send
   back.
5. Keep each question under 120 characters where possible.
6. Remove generic questions.
7. Remove questions that assign the user work already required from the
   assistant.
8. Remove questions that contradict an explicit user preference.

## 4. Append the nudge

1. Add one blank line after the substantive answer.
2. Use this exact lead-in:

```text
A few things worth a second look:
```

3. Add the questions as plain bullets.
4. Do not use a heading, blockquote, HTML, emoji, warning box, or closing
   invitation.
5. Put nothing after the final question.

## 5. Verify

1. Confirm that this is the first nudge in the conversation.
2. Confirm that the answer is actionable and substantive.
3. Confirm that every question names a concrete item from the answer.
4. Confirm that there are two or three questions.
5. Confirm that the exact lead-in appears once.
6. Confirm that the nudge is the final content.
