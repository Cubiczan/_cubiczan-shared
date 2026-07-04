#!/usr/bin/env python3
"""Update GitHub repo descriptions and topics for Cubiczan finance/governance stack."""
import json
import urllib.request

TOKEN = open("/dev/stdin").read().strip() if False else None

REPOS = {
    "Strata": {
        "description": "CFO maturity OS — rubric-graded assessments, 12 deliverable chains, 90-day roadmap (Streamlit + Python)",
        "topics": ["cfo", "finance", "fp-a", "ai-agents", "streamlit", "corporate-finance", "maturity-model", "governance"],
    },
    "Metabocommand": {
        "description": "Metabolic commerce multi-agent dashboard — capital reflex, approval queues, realtime agent action log (Next.js + Supabase)",
        "topics": ["cfo", "finance", "multi-agent", "ecommerce", "approvals", "supabase", "nextjs", "ai-agents"],
    },
    "consensus-hardening-protocol": {
        "description": "Consensus Hardening Protocol — adversarial review, lock-step verification, and auditable multi-agent decisions",
        "topics": ["ai-governance", "ai-safety", "consensus-protocol", "multi-agent", "adversarial", "decision-framework", "mcp", "compliance"],
    },
    "meshcfo": {
        "description": "Auditable multi-agent CFO — forecast, investment case, and board packets with CHP provenance",
        "topics": ["cfo", "multi-agent", "finance", "governance", "board-reporting", "chp", "ai-agents"],
    },
    "working-capital-optimizer": {
        "description": "AI agent mesh for AR/AP/inventory — shrink cash conversion cycle with Arize Phoenix eval loop",
        "topics": ["working-capital", "cfo", "cash-conversion-cycle", "ai-agents", "finance", "manufacturing"],
    },
    "cash-flow-optimizer": {
        "description": "13-week cash forecast + daily CFO brief — Xero, Precoro, Outlook, Vellum workflows",
        "topics": ["cash-flow", "cfo", "forecast", "xero", "finance", "ai-agents"],
    },
    "finance-cockpit": {
        "description": "CFO-grade Jira dashboard — budget, burn rate, runway, and working capital (Atlassian Forge)",
        "topics": ["jira", "cfo", "budget", "burn-rate", "atlassian-forge", "finance"],
    },
    "software-factory": {
        "description": "Cubiczan stack entry — automated feature factory with MAESTRO security gate and Render previews",
        "topics": ["ai-agents", "devops", "security", "superplane", "software-factory", "maestro"],
    },
    "cleanmandate": {
        "description": "Verified AI agent payment mandates — Cleanverse A-Pass, CCP, A-Token on Monad (Rust)",
        "topics": ["rust", "ai-agents", "compliance", "stablecoin", "monad", "travel-rule", "governance"],
    },
    "agent-conductor": {
        "description": "MCP agent conductor — AGENTS.md contracts, SKILL registry, CHP decision routing",
        "topics": ["mcp", "ai-agents", "orchestration", "governance", "typescript"],
    },
}
