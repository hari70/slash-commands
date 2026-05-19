Two-source weekly inbox processor: pulls new messages from registered Teams channels, classifies all unprocessed Granola notes, presents a unified candidate list, writes approved artifacts, and updates `_System/ingest-log.md` and channel cursors.

**Invocation forms:**
- `/process-inbox` — pull Teams + classify all unprocessed Granola notes
- `/process-inbox --status` — queue stats only, no pull or classification
- `/process-inbox --all` — re-review all files including already-processed
- `/process-inbox --granola` — Granola only, skip Teams pull
- `/process-inbox --teams` — Teams pull only, skip Granola queue

Read first (in order):
- `INDEX.md` — Active Clients canonical names
- `_System/teams-channels.md` — registered channels with cursors
- `_System/ingest-log.md` — processed filenames (create with header if missing)
- `_System/skills/process-inbox.md` — full skill spec (read completely)
- `_System/skills/promote-meeting.md` — file formats and signal criteria

Then follow process-inbox.md exactly. Key rules:

**Step 1 — Teams pull (for each active channel):**
Call `mcp__claude_ai_ms365__chat_message_search` with client name as query, limit 50.
Filter client-side: chatId matches channel ID + createdDateTime > cursor + not a bot sender.
Write qualifying messages to `Ingest/Teams/{ClientName}/YYYY-MM-DD-{subject-kebab}.md`.
Update cursor in teams-channels.md to newest message's createdDateTime.

**Step 2 — Granola queue:**
Glob `Ingest/Granola/*.md`. Unprocessed = not in ingest-log.md Filename column.

**Step 3 — Classification (per file, two-pass):**

For Granola files — meeting type (strict priority, stop at first match):
  INT in title → internal-about-client
  1:1 in title → internal-1on1
  CoP/Delivery Review/Weekly → internal-practice
  Client name + client person/ tags → customer-engagement
  External org, not known client → external-partner
  Client name + all-internal person/ tags → internal-about-client

For Teams files — meeting type: always `client-project-channel`
  Full artifact menu: ADR, Client Requirement, Client Context, Pattern, Intel
  ADR confidence starts HIGH when subject contains scope/decision language
  Client Context tagged `source: PM-relay` when PM is relaying client statements

**Always surface classifications before writing:**
Present all files in one unified view — Granola and Teams together, newest first.
Wait for architect confirmation before writing anything.

**After confirmation:**
Write approved artifacts using formats in promote-meeting.md.
Append log row per file to ingest-log.md (including skipped files).
Update channel cursors in teams-channels.md.

**Confidence gate for patterns:**
Medium → write to Patterns/, NOT indexed in INDEX.md.
High → write + add to INDEX.md.

All file formats in `_System/skills/promote-meeting.md`.
