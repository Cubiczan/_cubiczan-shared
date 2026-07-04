## Cubiczan stack

**Start here:** [software-factory](https://github.com/Cubiczan/software-factory) · [Profile](https://github.com/Cubiczan)

Cubiczan builds **auditable AI for finance and governance** — multi-agent systems where every recommendation traces to policy, reasoning, and human approval.

### Governance & orchestration

| Repo | Role |
|------|------|
| [consensus-hardening-protocol](https://github.com/Cubiczan/consensus-hardening-protocol) | CHP — adversarial review, lock states, probabilistic confidence |
| [agent-conductor](https://github.com/Cubiczan/agent-conductor) | MCP orchestration, SKILL registry, CHP decision routing |
| [compliance-as-code-agent](https://github.com/Cubiczan/compliance-as-code-agent) | YAML policy packs, scan/fix/validate, signed audit trails |
| [cleanmandate](https://github.com/Cubiczan/cleanmandate) | Verified agent payment mandates (Cleanverse A-Pass / CCP / A-Token) |

### Corporate finance

| Repo | Role |
|------|------|
| [Strata](https://github.com/Cubiczan/Strata) | CFO maturity assessment, rubric-graded deliverables, 90-day roadmap |
| [Metabocommand](https://github.com/Cubiczan/Metabocommand) | Metabolic commerce — capital reflex, approval queues, agent action log |
| [meshcfo](https://github.com/Cubiczan/meshcfo) | Auditable multi-agent CFO — forecast, investment case, board output |
| [working-capital-optimizer](https://github.com/Cubiczan/working-capital-optimizer) | AR/AP/inventory mesh — shrink cash conversion cycle |
| [cash-flow-optimizer](https://github.com/Cubiczan/cash-flow-optimizer) | 13-week forecast, Xero + Precoro + Outlook |
| [finance-cockpit](https://github.com/Cubiczan/finance-cockpit) | Jira budget, burn rate, runway dashboard |

### How they compose

```
Brief / mandate → CHP foundation + adversarial gate
       → specialist finance agents (Strata / MeshCFO / Metabocommand / WCO)
       → policy + compliance-as-code checks
       → human approval queue (CHP lock / Metabocommand / cleanmandate)
       → signed audit export
```

**Canonical org mirror:** [icohangar-ops](https://github.com/icohangar-ops) · **Codeberg:** [cubiczan](https://codeberg.org/cubiczan)

<!-- END:README_FOOTER — content below is internal tooling docs, NOT injected into repo READMEs -->

---

## Standard kit (`inject_stack.py`)

`inject_stack.py` is the rollout vehicle for the portfolio-wide **standard kit** —
one scripted sweep seeds each sibling repo with the governance + resilience
scaffolding so the whole portfolio converges on the same contract.

### What the kit injects

| Part | Writes | Behavior |
|------|--------|----------|
| `readme` | Cubiczan stack header + footer in `README.md` | original behavior; skips if the stack section already exists |
| `agents` | `AGENTS.md` contract (generalized from `agent-conductor`'s config-driven governance) | never clobbers an existing `AGENTS.md` unless `--force` |
| `chp` | `.chp/policy.yaml` (CHP decision policy with sane defaults) + `.chp/README.md` | writes only the two files it manages; leaves any other `.chp/*` files untouched |
| `resilience` | a dependency reference to `cubiczan-resilience` matched to the repo's language | conservative — see below |

The **resilience** part detects the repo language from its manifest and references
the right package:

| Manifest (checked in this order) | Language | Package |
|---|---|---|
| `Cargo.toml` | Rust | `resilient-call` |
| `package.json` | TypeScript | `@cubiczan/resilience` |
| `pyproject.toml` | Python | `cubiczan-resilience` |
| `requirements.txt` | Python | `cubiczan-resilience` |

Because publishing isn't set up, it writes a documented **local-path** reference
(a `RESILIENCE_ADOPT.md` note in every case, plus an appended comment in
comment-capable manifests). It never structurally edits a manifest: `package.json`
(JSON, no comments) is left entirely untouched — only the ADOPT note is written —
so no manifest is ever broken.

### CLI

```
python inject_stack.py [--kit PARTS] [--repos NAMES] [--apply] [--force]
                       [--selfcheck] [--list-repos]
```

- `--kit agents,chp,resilience` — comma-separated parts to inject
  (default: `agents,chp,resilience`; `readme` is opt-in).
- `--repos meshcfo,cleanmandate` — target a named list
  (default: **all** sibling repos, excluding `_cubiczan-shared`,
  `_cubiczan-updates`, `_AUDIT`, and `cubiczan-resilience` itself).
- `--apply` — actually write. **Omitting it is a dry-run** (safe default): the
  script prints exactly what *would* change and writes nothing.
- `--force` — overwrite existing managed files instead of skipping.
- `--selfcheck` — print detected language per repo and exit (verification aid).
- `--list-repos` — print discovered target repos and exit.

Idempotent: re-running skips files that already exist, and re-running with
`--apply` after a clean sweep is a no-op.

### Usage

```bash
# 1. See what a full sweep would do to the whole portfolio (dry-run, writes nothing):
python inject_stack.py

# 2. Sanity-check language detection:
python inject_stack.py --selfcheck

# 3. Apply just the AGENTS.md + .chp kit to a few repos for real:
python inject_stack.py --kit agents,chp --repos meshcfo,cleanmandate --apply

# 4. Wire the resilience reference across the portfolio:
python inject_stack.py --kit resilience --apply

# 5. Replace a stale AGENTS.md in one repo:
python inject_stack.py --kit agents --repos metabocommand --apply --force
```

