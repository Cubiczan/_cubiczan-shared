#!/usr/bin/env python3
"""Fetch the current EDGAR 8-K atom and print a JSON summary.

Fair-access User-Agent uses SEC_CONTACT_EMAIL. urllib is the primary path.
"""
from __future__ import annotations

import collections
import html
import json
import os
import re
import sys
import urllib.request
from xml.etree import ElementTree as ET

ATOM = (
    "https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent"
    "&type=8-K&company=&dateb=&owner=include&start=0&count=100&output=atom"
)
NS = {"a": "http://www.w3.org/2005/Atom"}
ITEM_RE = re.compile(r"Item\s+(\d+\.\d+)", re.I)


def fetch_atom() -> bytes:
    email = os.environ.get("SEC_CONTACT_EMAIL") or "sam@cubiczan.com"
    req = urllib.request.Request(
        ATOM,
        headers={
            "User-Agent": f"Cubiczan SEC Leads Daily ({email})",
            "Accept": "application/atom+xml,application/xml,text/xml,*/*",
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status == 403:
            raise SystemExit("EDGAR HTTP 403 (weekend/structural)")
        if resp.status != 200:
            raise SystemExit(f"EDGAR HTTP {resp.status}")
        return resp.read()


def parse(raw: bytes) -> dict:
    root = ET.fromstring(raw)
    entries = []
    item_counts: collections.Counter[str] = collections.Counter()
    date_counts: collections.Counter[str] = collections.Counter()
    for el in root.findall("a:entry", NS):
        title = el.findtext("a:title", default="", namespaces=NS) or ""
        link_el = el.find("a:link", NS)
        href = link_el.get("href") if link_el is not None else ""
        summary = el.findtext("a:summary", default="", namespaces=NS) or ""
        plain = html.unescape(re.sub(r"<[^>]+>", " ", summary))
        plain = re.sub(r"\s+", " ", plain).strip()
        filed = (re.search(r"Filed:\s*(\d{4}-\d{2}-\d{2})", plain) or [None, None])[1]
        acc = (re.search(r"AccNo:\s*([0-9-]+)", plain) or [None, None])[1]
        items = ITEM_RE.findall(plain)
        for item in items:
            item_counts[item] += 1
        if filed:
            date_counts[filed] += 1
        cm = re.match(r"^(8-K/?A?)\s*-\s*(.+?)\s*\((\d+)\)", title)
        entries.append(
            {
                "form": cm.group(1) if cm else "?",
                "company": cm.group(2).strip() if cm else title,
                "cik": cm.group(3) if cm else "",
                "filed": filed,
                "acc": acc,
                "items": items,
                "href": href,
            }
        )
    return {
        "title": root.findtext("a:title", default="", namespaces=NS),
        "updated": root.findtext("a:updated", default="", namespaces=NS),
        "count": len(entries),
        "dates": dict(date_counts),
        "item_tally": item_counts.most_common(),
        "entries": entries,
    }


def main() -> None:
    data = parse(fetch_atom())
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
