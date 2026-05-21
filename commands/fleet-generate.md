Generate a stack-tailored agent fleet for the current project from its Project Brief.

If `$ARGUMENTS` is provided as a file path, treat it as the Project Brief location. Otherwise default to `docs/PRD.md` in the current directory.

Special flags in `$ARGUMENTS`:
- `--update` — re-run generation against existing fleet (additive by default; ask before removing)
- `--brief <path>` — explicit brief location

## Execution

1. Read the methodology skill at `${VAULT_ROOT:-/Users/harit/AI-Projects/3cloud-vault/Hari_Work}/_System/skills/agent-fleet-generation.md` and follow it.

2. Read the Project Brief at the resolved path. Validate it exists, has frontmatter with `type`, and `status: approved`. If not approved, stop and ask the user to finalize the brief first.

3. Read the project lifecycle skill for context on which phase we're in: `${VAULT_ROOT:-/Users/harit/AI-Projects/3cloud-vault/Hari_Work}/_System/skills/project-lifecycle.md`

4. Analyze the brief and propose a fleet shape per the methodology. Format the proposal clearly:

```markdown
## Proposed Fleet for {Project Name}

Based on the brief, I recommend N agents:

**Core (always present):**
- lead-architect — orchestrator
- test-engineer — quality gate

**Generated based on stack:**
- <agent-name> — <one-line role>
- <agent-name> — <one-line role>

**Generated based on capability requirements:**
- <agent-name> — <one-line reason>

**Excluded:**
- <agent-name> (<reason>)

Proceed with this fleet, or adjust?
```

5. WAIT for explicit user approval. Do not generate before approval.

6. After approval, read templates from `${VAULT_ROOT:-/Users/harit/AI-Projects/3cloud-vault/Hari_Work}/Knowledge/Practice/AI-Engineering/Templates/agent-fleet/` for each approved role.

7. Generate each agent file by:
   - Filling `{{}}` placeholders with values extracted from the brief
   - Customizing the `{{STACK_EXPERTISE_BLOCK}}` per the project's stack declarations
   - Naming files: `<role>.md` for generic, `<stack-prefix>-<role>.md` for stack-tailored (e.g., `python-fastapi-backend-engineer.md`)
   - Writing to `./.claude/agents/`

8. Initialize or update `./.claude/lifecycle.json`:
   - First generation: phase `greenfield`, fleet_version `1.0`
   - Update mode: bump fleet_version, add phase_history entry if phase changed

9. Print summary report:

```markdown
## Fleet Generation Complete

Generated N agents in `.claude/agents/`:
- lead-architect.md
- <other agents>

Initialized `.claude/lifecycle.json` (phase: greenfield).

**Next steps:**
1. Review generated agents — adjust if needed
2. When ready to build: kick off Wave 1 (or run `/poc-builder` if greenfield)
3. After launch: use `/lifecycle-advance iteration` to enter Phase 2
```

## Constraints

- NEVER generate without user approval of the proposed fleet
- NEVER overwrite an existing fleet without explicit confirmation
- ONLY use templates from the vault's canonical location
- Add Cornell or 3Cloud-specific framework references ONLY if the brief is type `client-context` (work context). For `product-prd` (personal product), keep agents methodology-flavor-neutral.
