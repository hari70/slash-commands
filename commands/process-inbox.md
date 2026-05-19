Batch-process all unprocessed Granola notes in `Ingest/Granola/`. Classifies each note by meeting type, scans for promotable knowledge, presents a unified candidate list for architect review, writes approved artifacts, and marks each file processed in `_System/ingest-log.md`.

**Invocation forms:**
- `/process-inbox` — classify and promote all unprocessed notes
- `/process-inbox --status` — show queue stats only, no classification
- `/process-inbox --all` — re-review all notes including already-processed ones

Read first (in order):
- `INDEX.md` — Active Clients canonical names, Patterns/Architectural file list
- `_System/ingest-log.md` — processed filenames (create with header if missing)
- `_System/skills/process-inbox.md` — full skill spec (read completely before proceeding)
- `_System/skills/promote-meeting.md` — file formats and signal criteria

Then follow process-inbox.md exactly. Key rules:

**Queue detection:**
Compare `Ingest/Granola/*.md` filenames against `_System/ingest-log.md` Filename column.
Unprocessed = in Ingest/ but not in log. Sort newest-first by created_at.

**Classification (per note, two-pass):**
Pass 1 — meeting type (strict priority, stop at first match):
  INT in title → internal-about-client
  1:1 in title → internal-1on1
  CoP/Delivery Review/Weekly/Practice → internal-practice
  Client name + client person/ tags → customer-engagement
  External org, not known client → external-partner
  Client name + all-internal person/ tags → internal-about-client

Pass 2 — content signal scan → ADR / Client Requirement / Architecture Pattern /
  Client Context Update / Market Intel / Skip

**Always surface classifications before writing:**
Present all files and candidates in one unified view. Wait for confirmation.

**After writing:**
Append one log row per file to `_System/ingest-log.md` — including skipped files.
A skipped file = reviewed and consciously passed, not ignored.

**Log row format:**
| YYYY-MM-DD | filename | meeting-type | promoted N / skipped | artifact list or "none" |

All file formats are in `_System/skills/promote-meeting.md`. Confidence gate:
Medium patterns → write to Patterns/, NOT indexed. High → write + add to INDEX.md.

Final report:
```
Inbox processed — N notes reviewed

  Promoted: {artifact list}
  Skipped: {filename list with reason}
  Log updated: _System/ingest-log.md

N medium patterns pending — run /promote-meeting --review to promote.
```
