# CampusFlow — AI-Native Engineering Learning Log

**Project:** CampusFlow | **Sprint:** 12 October 2026 | **Fellows:** Vejeh and Gideon

> **Evidence standard:** This log reconstructs work from the team's ChatGPT conversation, code excerpts, GitHub commits, and terminal screenshots. It is **not** a verbatim transcript of every AI prompt. Where a prompt or Gideon's own experiment was not shared, the entry is marked **needs fellow confirmation** rather than invented. Reviewers should not interpret a reconstructed engineering discussion as proof that Gideon personally performed a specific AI experiment.

## Vejeh — verified learning interactions

### 1. Priority algorithm and boundary tests
**Concept:** Deterministic first-match decision logic in Python; using `unittest` to test boundaries.

**Interaction:** Asked for step-by-step guidance implementing and testing `calculate_priority()`. Initially answered the priority exercise as `high`. Developed tests for `("high", 12) → "critical"`, `("high", 10) → "critical"`, `("high", 9) → "high"`, `("high", 2) → "high"`, `("low", 4) → "medium"`, `("low", 1) → "low"`, and `("medium", 15) → "high"`.

**Independent verification:** Terminal screenshot first showed **5 passing tests**, then **7 passing tests** after adding uniquely named boundary methods. An early pasted test snippet reused `test_critical_priority` three times; that would cause earlier definitions to be overwritten in a Python class. The subsequent screenshot showed distinct test method names and seven discovered tests.

**Learning:** Test names must be unique; priority rules are ordered and inclusive at the 10-user critical threshold. Test both sides of a boundary rather than only representative inputs.

### 2. Input validation and composing validated functions
**Concept:** Validation, normalization, exceptions, Python type checking and the `bool` subclass of `int`.

**Interaction:** Built `validate_title`, `validate_category`, `validate_urgency`, and `validate_affected_users`. Shared tests for blank/non-string titles, case and whitespace normalization, invalid categories/urgencies, zero and negative affected-user counts, boolean and floating-point values. Added an integration test feeding the normalized urgency `"HIGH"` into the priority calculation.

**Independent verification:** Terminal screenshots showed **12**, **21**, **22**, then **25 passing tests** as cases were added. A code excerpt showed explicit rejection of boolean affected-user counts with `type(affected_users) is not int`.

**Learning:** Validate before mutating the ticket collection; normalize accepted user inputs to a consistent representation; ensure booleans are not accepted as user counts.

### 3. Ticket creation, JSON persistence and critical evaluation of AI-assisted test design
**Concept:** ID generation, state mutation, `unittest`, safe JSON writes, schema validation and test-driven debugging.

**Interaction:** Implemented `generate_ticket_id()` by finding the highest existing numeric ID, then `create_ticket()` with normalized fields and calculated priority. Built `load_tickets()` and `save_tickets()` using `pathlib`, `json`, a temporary file, and `os.replace()`. Tested round-tripping, malformed JSON, unique IDs after reload, and failure to serialize invalid data.

**Critical evaluation / correction:** A later expanded storage test suite exposed **7 failures and 1 error among 44 tests**. The error arose because a list-valued ticket ID was checked for membership in a set before its type was validated (`TypeError: unhashable type: 'list'`). The failures showed missing validation of blank titles, invalid IDs/urgency/status, inconsistent priority and unassigned in-progress tickets. Vejeh then shared a revised `validate_stored_tickets()` implementation enforcing additional invariants. A screenshot confirmed **44 tests passing**, followed by **49 passing tests** after further storage cases.

**Learning:** Passing earlier tests did not establish that persisted records were trustworthy. Invalid stored data must be rejected before it reaches workflow logic; validation order matters because malformed types can cause unintended exceptions. Atomic replacement helps preserve an existing file when serialization fails.

**Verified outcomes:** Screenshots also showed **29**, **32**, **34**, and **36** tests during development. Later, the integrated CLI and modules produced **78 passing tests**, then **84 passing tests** with six CLI integration tests. Vejeh launched `python3 main.py` and successfully listed an existing ticket (`T001 | Mouse Issue`) loaded from JSON.

## Gideon — work and corrections observed in shared repository

The following are **code review / integration observations**, not three verified personal AI-learning interactions by Gideon. His actual AI prompts, predictions, independent experiments and takeaways must be confirmed by Gideon if the assessment requires individual evidence.

### Observed engineering topic A — Assignment validation
**Implementation:** `campusflow/workflow.py` includes staff assignment and workflow transitions.

**Review finding and correction:** Earlier review identified weaknesses in staff-name type checking and whitespace normalization. A subsequent branch review confirmed these had been addressed.

**Evidence:** Gideon's `feat/2-workflow-queue-reports` branch and the subsequent integration review.

**Gideon to confirm:** What question he asked AI, what example he independently ran, and what result he observed.

### Observed engineering topic B — Workflow, priority queue and tests
**Implementation:** Assignment, status lifecycle, reopen operation and open-ticket queue. The workflow test file contained **22 tests** in the reviewed branch.

**Review finding:** A `make_ticket()` fixture hardcoded `urgency="high"` and `affected_users=5` while allowing arbitrary priority values, producing records inconsistent with the ticket engine's priority rules. The review recommended mapping each priority to consistent urgency and affected-user inputs, as already done in the report tests. This is a **known review observation**, not evidence the fixture was later corrected.

**Gideon to confirm:** His own test experiment and whether he made the fixture correction.

### Observed engineering topic C — Reporting and repository hygiene
**Implementation:** `campusflow/reports.py` provides report totals and breakdowns; `tests/test_report.py` contained **7 tests** in the reviewed branch.

**Review findings and corrections:** Added dedicated report tests, normalized fixture category values, and removed Python bytecode files from the current changes. A shared terminal comparison showed Gideon's branch introducing workflow/report modules and tests. The integrated suite later passed **78 tests**, including the existing feature tests.

**Gideon to confirm:** His own AI interaction and independently verified correction, if any.

## Collaboration, review and integration evidence

- **Repository:** https://github.com/Vict1111-code/campusflow
- **Vejeh's feature branch:** `feat/1-ticket-engine-storage`
- **Gideon's feature branch:** `feat/2-workflow-queue-reports`
- **Integrated branch:** `integration/campusflow-reviewed`
- **Draft integration PR:** https://github.com/Vict1111-code/campusflow/pull/2
- **Observed review comments/findings:** staff-name normalization/type checks; reporting test coverage; fixture consistency; bytecode-file hygiene.
- **Merge obstacle:** A local `.gitignore` add/add conflict arose when combining feature branches. The conflict was avoided by constructing a separate GitHub integration branch with reconciled ignore rules, without changing `master`.
- **Test evidence:** Vejeh's terminal screenshot: `python3 -m unittest discover -s tests -v` → **78 tests, OK**. After adding the CLI and its six tests, screenshot: **84 tests, OK**.
- **CLI evidence:** `python3 main.py` opened the interactive menu and displayed a persisted `T001` ticket.
- **Still required:** Human review/approval records, Gideon's own AI learning evidence, full manual lifecycle/restart demonstration, and final tests on `master` after an approved merge.

## Short technical defence notes

**Vejeh:** Explain why critical must be checked before high; why `bool` is rejected as an affected-user count; how ID generation remains unique after reload; why invalid JSON and invalid stored records are rejected; why the storage writer uses a temporary file and `os.replace()`; and what the 44-test failures taught about validation order.

**Gideon:** Explain the assignment guard; the permitted state transitions; why resolved tickets require explicit reopening; how open tickets are sorted by priority and numeric ID; why queue operations must not mutate the original ticket list; and why workflow fixtures must match the ticket schema.

## Accuracy note
This log uses documented events and test outputs. It intentionally does not fabricate exact AI prompts, private experiments, reciprocal human approvals, or claims that Gideon personally used AI in a particular way. Gideon should confirm or add his individual evidence before final submission.
