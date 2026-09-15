# Cursor automation — SEC leads daily

Dashboard: [SEC LEADS FILING AGENT](https://cursor.com/automations/0980e453-a3b6-11f1-a7d1-d6b4613131ce)

## Required settings

- **Repo-backed.** The ledger has to persist. Point the automation at **Cubiczan/_cubiczan-shared** (this repo) so `AGENTS.md` and `ledger/sends.jsonl` are on disk. `icohangar-ops/_cubiczan-shared` is archived/read-only — a push there 403s.
- **Prompt:** Follow `AGENTS.md` — screen, verify filings directly, write the digest, send via Customer.io, append the ledger only after `SENT — delivery_id …`.
- **Two crons:**
  - 07:00 ET (`0 11 * * *` UTC while EDT)
  - 13:00 ET catch-up (`0 17 * * *` UTC). No-op if `ledger/sends.jsonl` already has today’s digest `delivery_id`.

Weekend 403s are structural. Same human gate: paste-ready openers; a human approves before any outreach.

## Environment

Put these on the Cursor environment / automation secrets (never in chat or git):

| Need | Name |
| --- | --- |
| Required to send | `CUSTOMERIO_APP_API_KEY` |
| Already known | `DIGEST_FROM` / `DIGEST_TO` |
| Required for EDGAR | `SEC_CONTACT_EMAIL` |
| Optional | `TAVILY_API_KEY`, `EXA_API_KEY`, `CUSTOMERIO_REGION`, `CUSTOMERIO_TRANSACTIONAL_MESSAGE_ID` |

Do not send: Gmail app password, Gmail OAuth, Firecrawl, You.com, Nimble, Brevo.
