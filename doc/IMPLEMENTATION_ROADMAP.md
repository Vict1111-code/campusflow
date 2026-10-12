# CampusFlow — Implementation Roadmap

## Delivery target
Six-hour two-fellow Python CLI sprint. Documentation is preparation; implementation, review and test evidence must be produced during the actual sprint.

## Dependency graph
```text
Repo setup → shared ticket schema/contracts → parallel work
                                      ├→ Victor: validation → priority → creation → persistence → CLI
                                      └→ Gideon: assignment → lifecycle → queue → reports
Both feature branches → reciprocal PR reviews → approved merges → integration tests → demo
```

## Phase 1 · 00:00–00:20 · GitHub setup
- Confirm `Vict1111-code/campusflow`, current default branch `master`, collaborator permissions, identity and local clones.
- Add `.gitignore` for `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `data/tickets.json`.
- No direct implementation commits to `master`.
- Evidence: repository URL, collaborators, initial commit.

## Phase 2 · 00:20–00:50 · Design/contracts
- Read PRD and owner documents together.
- Open GitHub Issues for creation/validation/priority, storage/CLI, assignment/lifecycle, queue/reports and tests.
- Agree on ticket container, function signatures, return values, exception policy, save triggers, next-ID strategy and reopen semantics.
- Write `doc/design-decisions.md` before parallel implementation.
- Evidence: issue links and signed-off decisions.

## Phase 3 · 00:50–01:30 · AI learning
- Each fellow chooses two uncertain concepts and performs two small independent experiments unrelated to CampusFlow.
- Record actual prompt, prediction, experiment, observed result and explanation.
- During coding add a third verified interaction; at least one must critically improve or reject AI guidance.
- Evidence: individual entries in `doc/ai-learning-log.md`.

## Phase 4 · 01:30–03:55 · Parallel implementation
### Victor (larger/harder scope)
1. Validation and canonical normalization.
2. Priority first-match engine and ticket creation/lookup/unique IDs.
3. JSON read/write and restart-safe IDs, explicit malformed JSON errors.
4. Repeating CLI menu and integration wiring.
5. `tests/test_tickets.py`, `tests/test_storage.py`; include boundaries and malformed data.

### Gideon (smaller scope)
1. Assignment by ID, blank staff rejection.
2. Lifecycle guards and explicit reopen.
3. Open queue sorting by priority then numeric ID.
4. Reports including empty store.
5. `tests/test_workflow.py`, `tests/test_reports.py`.

### Integration contract
Do not import CLI prompts into domain modules. Gideon's functions operate on the agreed ticket collection; Victor's CLI calls them. Use short commits on individual branches. Run relevant tests before each push.

## Phase 5 · 03:55–05:00 · PRs and review
- Victor opens PR against `master`; Gideon reviews with at least two substantive observations.
- Gideon opens PR against `master`; Victor reviews with at least two substantive observations.
- Fix blockers on the same branch, rerun tests, seek final approval, then merge.
- If the second branch is behind, merge latest `master` into it, resolve conflicts, rerun tests and re-review final diff.
- Evidence: both PR links, review threads, approvals, merge commits.

## Phase 6 · 05:00–05:40 · Integration
- On latest `master`: `python main.py` and `python -m unittest discover -s tests -v`.
- Manual flow: create 4 priority examples; reject zero users; assign; progress; reject unassigned transition; reopen; show queue/report; restart; confirm IDs; try malformed JSON using a separate disposable file.
- Fix via reviewed PR, not unreviewed direct default-branch commits.
- Update README, decisions, AI log, limitations and test evidence.

## Phase 7 · 05:40–06:00 · Demo/defence
- Both fellows speak and demonstrate their own feature and test.
- Each explains an AI suggestion verified/improved/rejected and a partner PR review.
- Present repository, two PR links, passing test output, and JSON persistence demo.

## Milestones / exit gates
| Gate | Required evidence |
|---|---|
| G1 Ready | Both clones/collaborator access |
| G2 Designed | Issues + agreed contracts |
| G3 Learned | Two initial AI experiments each |
| G4 Built | Feature branches + own tests + three logs each |
| G5 Reviewed | Reciprocal substantive review + approval |
| G6 Integrated | All seven features + >=8 passing tests on master |
| G7 Submitted | Live demo, documentation, repo/PR links |

## Risks and mitigations
- Contract mismatch: freeze interfaces before coding and use sample fixture.
- Race on shared files: strict module ownership; agree before touching shared files.
- Insufficient test coverage: prioritize invalid/boundary cases, not just happy paths.
- JSON data loss: never treat malformed JSON as empty; verify before writes.
- Git review delays: reserve full review window and push early.
- Overengineering: standard library CLI only.

## Out of scope
GUI, web frontend, REST API, external database, authentication, hosted deployment, and AI inference inside CampusFlow.
