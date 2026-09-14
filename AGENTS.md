# SEC leads daily agent

Screen the live EDGAR 8-K feed, verify filings directly, write a digest, send it
through Customer.io, and append `ledger/sends.jsonl` only after `SENT — delivery_id …`.

This automation is repo-backed so the send-once ledger can persist. The stalled-pilot
news lane is retired; the digest runs on EDGAR.

## Loop

1. If `ledger/sends.jsonl` already has a **digest** `delivery_id` for today’s ET date, stop (catch-up no-op). Wiring-test and blocked-run status rows do not count.
2. Fetch the current 8-K atom (`count=100`) with a fair-access User-Agent that includes `SEC_CONTACT_EMAIL`.
3. Weekend HTTP 403s are structural: send a short status email, do not invent leads, do not outreach.
4. Parse items. High-signal first: **5.02** (CFO / principal finance seat), **2.01**, **1.01** (financing / merger that changes the finance stack). Ignore 9.01-only, 8-K/A housekeeping, SPACs, and receivable trusts unless a finance-seat change is explicit.
5. Open the primary 8-K (complete submission `.txt` or HTML) and verify the item body. Atom titles are not enough.
6. Write paste-ready openers. **A human approves before any outreach.**
7. Send the digest via Customer.io App API (`scripts/send_digest.py`). From `DIGEST_FROM` (verified sender) to `DIGEST_TO`.
8. Append one JSONL row to `ledger/sends.jsonl` only after the API returns a `delivery_id`.

## Send-once / delivered-memory gap

The ledger in this repo starts from this automation’s own sends plus any imported
outreach packs. It is **not** the prior scout’s 154-company memory.

Until that full list is imported: **do not treat “not in this file” as “never delivered.”**
Say so in every digest. Do not recommend first-touch outreach on that basis.

## Mailer

- `POST https://api.customer.io/v1/send/email` (US). Use `https://api-eu.customer.io/v1/send/email` only when `CUSTOMERIO_REGION=eu`.
- Bearer `CUSTOMERIO_APP_API_KEY` (App API key, not Track/Site).
- JSON: `to`, `from`, `subject`, `body` (raw HTML), `identifiers.email` (the `to` address).
- Optional `CUSTOMERIO_TRANSACTIONAL_MESSAGE_ID` only if a saved template should replace the raw body.
- Do not print the API key. Do not use Gmail, Firecrawl, You.com, Nimble, or Brevo.

## Secrets / env

Required to send: `CUSTOMERIO_APP_API_KEY`.  
Already known: `DIGEST_FROM=sam@impactquadrant.info`, `DIGEST_TO=sam@cubiczan.com`.  
Required for EDGAR: `SEC_CONTACT_EMAIL` (not a secret).  
Optional: `TAVILY_API_KEY` (news only), `EXA_API_KEY` (JS-shell SEC pages; urllib is primary), `CUSTOMERIO_REGION`, `CUSTOMERIO_TRANSACTIONAL_MESSAGE_ID`.

## Cron (intended)

- 07:00 ET: `0 11 * * *` UTC while EDT
- 13:00 ET catch-up: `0 17 * * *` UTC

Settings live in `docs/cursor-automation.md`.
