Read a Granola meeting note from `Ingest/Granola/` and promote durable knowledge into the right vault location — ADRs, client requirements, architecture patterns, client context updates, or market intel — based on meeting type and content signals.

**Invocation forms:**
- `/promote-meeting {partial-filename}` — promote a specific Granola note
- `/promote-meeting --client KeyBank {partial-filename}` — override client inference
- `/promote-meeting --review` — batch review all pending medium-confidence patterns

Read first (in order):
- `INDEX.md` — for Active Clients canonical names and Patterns/Architectural file list
- `_System/skills/promote-meeting.md` — the full skill spec (read completely before proceeding)

Then follow the skill spec exactly. Key rules:

**Classification before writing — always:**
Surface the full candidate list with proposed artifact types and ask for confirmation before writing a single file.

**Two-pass classification:**
1. Meeting type from frontmatter (customer-engagement / internal-1on1 / internal-practice / external-partner) → determines which artifact types are on the menu
2. Content signal scan of body → classifies each extractable item

**Five artifact types and their destinations:**
- ADR → `Clients/{name}/Architecture-Decisions/ADR-NNN.md` (client-level, never per-engagement)
- Client Requirement → `Clients/{name}/Engagements/{slug}/Requirements.md` (append, single file)
- Architecture Pattern → `Knowledge/Architecture/Patterns/Architectural/{Name}.md`
- Client Context Update → append to `Clients/{name}/Client Context.md`
- Market/Practice Intel → `Knowledge/Strategy/Research/{slug}.md`

**Confidence gate for patterns:**
- Medium → written to Patterns/ with draft frontmatter; NOT added to INDEX.md
- High → written + added to INDEX.md (visible to all skills)
- Inline promotion: at extraction time, ask architect to confirm medium-confidence patterns
- Cross-meeting corroboration: if same pattern appears in 2+ meetings, offer upgrade to High
- `--review` mode: batch list all Medium patterns for architect sign-off

**ADR numbering:** scan `Clients/{name}/Architecture-Decisions/` for highest existing number, auto-increment, zero-pad to 3 digits.

**Requirements numbering:** scan existing `Requirements.md` for last REQ-NNN, auto-increment.

**Pattern numbering:** scan frontmatter of `Knowledge/Architecture/Patterns/Architectural/*.md` for highest `pattern_id`, increment.

**Never:**
- Write anything before architect confirms the classification list
- Touch the source Granola note
- Invent reasons or tradeoffs not in the meeting text
- Add Medium-confidence patterns to INDEX.md
- Store patterns inside Clients/ folders
- Create per-engagement ADR subfolders

All file formats (ADR, Requirements, Pattern, Client Context, Market Intel) are in `_System/skills/promote-meeting.md`. Read them before writing.

Final report format:
```
Promoted {N} items from {filename}

  ADRs: {list}
  Requirements: {list}
  Patterns: {list with confidence level}
  Client Context: {list}
  Market Intel: {list}

Source: Ingest/Granola/{filename} (untouched)
Run /promote-meeting --review to batch-promote pending medium patterns.
```
