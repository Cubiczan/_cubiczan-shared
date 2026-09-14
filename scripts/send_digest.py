#!/usr/bin/env python3
"""Send the SEC leads digest through the Customer.io App API.

Reads CUSTOMERIO_APP_API_KEY from the environment. Does not print it.
Dry-run with --dry-run (prints subject + body length only).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def api_base(region: str) -> str:
    if region.lower() == "eu":
        return "https://api-eu.customer.io/v1"
    return "https://api.customer.io/v1"


def send_email(*, subject: str, body: str, dry_run: bool = False) -> dict:
    key = os.environ.get("CUSTOMERIO_APP_API_KEY") or ""
    to_addr = os.environ.get("DIGEST_TO") or "sam@cubiczan.com"
    from_addr = os.environ.get("DIGEST_FROM") or "sam@impactquadrant.info"
    region = os.environ.get("CUSTOMERIO_REGION") or "us"
    tx_id = os.environ.get("CUSTOMERIO_TRANSACTIONAL_MESSAGE_ID") or ""

    payload: dict = {
        "to": to_addr,
        "from": from_addr,
        "subject": subject,
        "identifiers": {"email": to_addr},
    }
    if tx_id:
        payload["transactional_message_id"] = tx_id
    else:
        payload["body"] = body

    if dry_run:
        return {
            "dry_run": True,
            "to": to_addr,
            "from": from_addr,
            "subject": subject,
            "body_chars": len(body),
            "region": region,
        }

    if not key:
        raise SystemExit("CUSTOMERIO_APP_API_KEY is not set")

    req = urllib.request.Request(
        f"{api_base(region)}/send/email",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Customer.io HTTP {exc.code}: {detail[:400]}") from exc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    body = open(args.body_file, encoding="utf-8").read()
    result = send_email(subject=args.subject, body=body, dry_run=args.dry_run)
    # Never dump headers or the key. delivery_id is the only secret-adjacent field we keep.
    if args.dry_run:
        print(json.dumps(result))
        return
    delivery_id = result.get("delivery_id") or (result.get("delivery") or {}).get("id")
    queued_at = result.get("queued_at")
    if not delivery_id:
        print(json.dumps({"ok": False, "keys": sorted(result.keys())}))
        sys.exit(2)
    print(f"SENT — delivery_id {delivery_id}" + (f" queued_at {queued_at}" if queued_at else ""))


if __name__ == "__main__":
    main()
