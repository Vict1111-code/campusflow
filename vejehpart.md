# Victor Ejeh — Engineering Work Package (Lead / Harder Scope)

**Owner:** Victor (Engineer A / integration lead). **Relative scope:** larger and more technically coupled. **Partner:** Gideon. Read `PRD.md` and `AGENT.md` first.

## Mission
Own the foundation and integration: validation, deterministic priority, ticket creation/lookup, unique ID management, safe JSON persistence, CLI menu, and final integration. Implement and test your own code; do not take over Gideon's assigned business modules.

## Owned files
- `campusflow/tickets.py`: validation, priority, create/list/lookup, ID generation.
- `campusflow/storage.py`: JSON load/save and safe errors.
- `main.py`: repeating CLI and wiring to both engineers' functions.
- `tests/test_tickets.py` and `tests/test_storage.py`: own tests.
- Integration coordination; shared `docs/design-decisions.md` with Gideon's agreement.

## Work breakdown
### V1 Agree interfaces before code (blocking)
Decide with Gideon: list of dictionaries vs ID map; whether functions mutate/return records; error policy; IDs and storage strategy; who calls save; allowed reopen behavior. Record signatures and a shared sample ticket.

### V2 Validation and priority
- Reject blank title, unsupported category/urgency, invalid affected_users (including `bool`, zero, negative, float, text).
- Accept case variants and normalize canonical values.
- Implement first-match priority exactly as PRD; never ask AI to decide priority.
- Tests: four priority cases, boundary 10, invalid values, case normalization.

### V3 Creation, listing, lookup and IDs
- Create ticket with all eight fields, unique sequential T-prefixed ID, open status, null assignee.
- Ensure invalid creation cannot partially mutate collection.
- Provide list/view and unknown-ID error.
- Ensure IDs do not collide after loading saved tickets.

### V4 Persistence
- Load missing file as fresh empty state.
- Malformed JSON must surface clear error; never silently erase.
- Save and load ticket records preserving fields; create after reload without duplicate ID.
- Consider atomic temporary-file replace; test with temporary directories, not real runtime data.

### V5 CLI / integration
- Loop menu until Exit; create, list, view, assign, change status, reopen, queue, report.
- Catch domain/storage errors at the CLI boundary with useful messages.
- Invoke Gideon's functions using agreed signatures; don't reimplement them.
- Decide and document when saves occur; ensure restart persistence.

## Branch and PR
Use a descriptive issue-numbered branch, e.g. `feat/1-ticket-core-storage-cli` (replace number with actual Issue). Commit in increments. Open a PR to `master` with requirements, changed files, actual tests, and risks. Gideon must review and approve before merge. Review Gideon's PR separately with two substantive observations.

## Acceptance checklist
- [ ] All four required priority examples correct.
- [ ] Invalid inputs rejected without mutation.
- [ ] Unique IDs on creation and after reload.
- [ ] Missing JSON file handled; malformed JSON surfaced safely.
- [ ] CLI exposes all seven features and exits cleanly.
- [ ] Own automated tests written and run.
- [ ] Own three verified AI learning entries, one critically evaluated.
- [ ] Own PR authored; Gideon's PR reviewed substantively.
- [ ] Can explain priority ordering, persistence safety and integration choices.

## Handoff to Gideon
Provide approved ticket schema, function signatures, exception conventions, sample fixture and working import path early. Confirm Gideon's modules are callable before integrating the CLI. Do not merge or rewrite Gideon's feature branch yourself.

## Suggested AI learning topics
`json.load` vs `json.dump`; exception handling; atomic file replacement; `unittest.mock` and temporary directories; designing pure functions. Experiment with unrelated examples and record real outcomes.
