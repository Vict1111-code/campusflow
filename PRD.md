# CampusFlow — Product Requirements Document (PRD)

## 1. Problem and objective
Learn2Earn campus staff receive Wi-Fi, hardware, software, and platform support requests. Informal reporting loses incidents and obscures ownership. Build a reliable Python CLI that creates, prioritizes, assigns, tracks, lists, reports, and persists support tickets.

## 2. Users and boundaries
Primary operator: campus IT/helpdesk staff. This is a local command-line tool, not a multiuser service. No login, GUI, HTTP API, AI-based priority model, or database is required.

## 3. Data contract
Each ticket contains exactly the required logical fields:
- `id`: unique automatically generated string `T001`, `T002`, ...
- `title`: nonblank string (trim whitespace)
- `category`: Network, Hardware, Software, Other (case-insensitive input; canonical output)
- `urgency`: low, medium, high (case-insensitive input; lowercase output)
- `affected_users`: strictly positive integer; reject zero, negatives, decimals, text and booleans
- `priority`: critical, high, medium, low (derived, never manually chosen)
- `status`: open, in_progress, resolved (new tickets begin open)
- `assigned_to`: null initially, otherwise nonblank staff name

Example:
```json
{"id":"T001","title":"Campus Wi-Fi is down","category":"Network","urgency":"high","affected_users":15,"priority":"critical","status":"open","assigned_to":null}
```

## 4. Priority rules — FIRST match wins
1. `urgency == high AND affected_users >= 10` → `critical`
2. `urgency == high OR affected_users >= 10` → `high`
3. `urgency == medium OR affected_users >= 3` → `medium`
4. Otherwise → `low`

Examples: (high,12) critical; (high,2) high; (low,4) medium; (low,1) low. The engine is ordinary deterministic Python logic.

## 5. Functional requirements
### F1 Create
Prompt for title, category, urgency, affected_users; validate before mutation; generate a never-reused ID after reload; calculate priority; set status open and assigned_to null. Invalid entries produce actionable errors and no partial ticket.

### F2 List / View
List all tickets and retrieve one by exact ID. Unknown IDs return clear errors. Empty list is handled gracefully.

### F3 Assign
Assign existing ticket to nonempty staff name. Reject unknown ID. A resolved ticket cannot be modified until explicitly reopened.

### F4 Lifecycle
Valid progression: open → in_progress → resolved. Reject in_progress on unassigned ticket; reject skipping stages, backward transitions and changes to resolved tickets without an explicit reopen operation that sets status open. Reopen must be deliberate and testable.

### F5 Queue
Show **open** tickets only, ordered by priority critical > high > medium > low, ties by ascending numeric ID. An in_progress ticket is unresolved but is **not** open; the source explicitly requests the open-ticket queue.

### F6 Reports
Display total ticket count, counts per status and counts per priority. Zero tickets must produce zeros rather than errors.

### F7 Persistence
Save to JSON and reload on startup. Missing file means empty store. Malformed JSON must surface an error, never silently reset or overwrite existing data. Preserve IDs and compute next ID safely after reload. Avoid partial writes where feasible.

### CLI
Menu repeats until Exit. Menu actions expose all seven features including viewing one ticket, reopening, and saving/reloading behavior. Keep interaction in `main.py`; core logic must be independently unit-testable.

## 6. Nonfunctional requirements
- Python standard library (`json`, `unittest`, `pathlib`, etc.).
- Clear error messages; no corruption on invalid operations.
- Separate core functions from `input()`/`print()` to enable tests.
- JSON runtime file excluded from version control.
- Both fellows contribute code, tests, and reviewed PRs.

## 7. Acceptance test matrix
| ID | Scenario | Expected |
|---|---|---|
| A01 | high, 12 users | critical |
| A02 | high, 2 users | high |
| A03 | low, 4 users | medium |
| A04 | low, 1 user | low |
| A05 | affected_users = 0 | reject without mutation |
| A06 | blank title/invalid category or urgency | reject |
| A07 | unassigned open → in_progress | reject |
| A08 | assigned open → in_progress → resolved | allow |
| A09 | resolved modification without reopen | reject |
| A10 | explicit reopen | status becomes open |
| A11 | queue with priority ties | priority then numeric ID |
| A12 | empty reports | zero totals and breakdowns |
| A13 | JSON save and restart | data preserved |
| A14 | create after reload | no duplicate ID |
| A15 | malformed JSON | clear error, data not erased |
| A16 | unknown ticket ID | clear error |

## 8. Delivery and assessment
100 marks: functionality 40, testing 15, professional Git workflow 20, AI-native engineering 20, technical defence 5. Minimum eight meaningful automated tests on integrated default branch. Two authored PRs with genuine reciprocal reviews and approvals. Each fellow documents at least three verified AI interactions, one involving an independently improved/rejected suggestion. Both defend own work.

## 9. Decisions to confirm jointly
Use a list of ticket dictionaries or a dictionary indexed by ID; exact function signatures; error strategy; when persistence occurs; corrupted-schema handling; reopening semantics; who implements CLI integration. Record final decisions in `docs/design-decisions.md`. Recommendations in this PRD are implementation guidance, not additional assessment requirements.
