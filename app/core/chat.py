"""Legal Assistant Chat Engine for PlainClause.

Provides intelligent responses for common contract and legal document analysis queries.
"""

from __future__ import annotations

import re
from typing import Dict, List, Any, Tuple

# Pre-built Knowledge Base for contract queries
KNOWLEDGE_BASE: List[Tuple[List[str], str, List[str]]] = [
    (
        ["non-compete", "non compete", "compete clause", "restrictive covenant"],
        "A **Non-Compete Clause** restricts you from working for a competitor or starting a competing business after leaving an employer. Key things to check:\n\n"
        "• **Duration**: Is it reasonable (e.g. 3-6 months vs 2+ years)?\n"
        "• **Geographic Scope**: Is it limited to your city/region or global?\n"
        "• **Industry Scope**: Is it narrowly focused on your role or blanket across all tech/business?",
        [
            "How long is a typical non-compete?",
            "What is IP assignment?",
            "What is a non-solicitation clause?",
        ],
    ),
    (
        ["security deposit", "deposit refund", "deposit deduction", "housing deposit"],
        "A **Security Deposit Clause** outlines the money paid upfront to cover property damage or unpaid rent. Red flags to watch out for:\n\n"
        "• **Automatic Retention**: Clauses allowing the landlord to keep the deposit for early exit without justification.\n"
        "• **Return Timeline**: Ensure a fixed deadline (e.g. 14-30 days) for return with an itemized receipt of deductions.\n"
        "• **Move-in Inventory**: Always take dated photos on day 1 to protect your deposit.",
        [
            "Can a landlord enter without notice?",
            "What is a rent increase clause?",
            "What is a notice period?",
        ],
    ),
    (
        ["indemnification", "indemnity", "indemnify", "hold harmless"],
        "An **Indemnification Clause** requires one party to pay for the losses, legal fees, or damages incurred by the other party. Critical tips:\n\n"
        "• **Mutual vs Unilateral**: Unilateral indemnities force only *you* to pay. Negotiate for mutual indemnity.\n"
        "• **Liability Caps**: Ensure your indemnity obligation is capped at contract value or insurance policy limits.\n"
        "• **Exclusions**: Exclude gross negligence or willful misconduct of the other party.",
        [
            "What is a limitation of liability?",
            "What is termination for convenience?",
            "What are payment terms?",
        ],
    ),
    (
        ["arbitration", "dispute resolution", "class action waiver", "sue in court"],
        "A **Mandatory Arbitration Clause** forces disputes to be resolved by a private arbitrator instead of a public court. Points to note:\n\n"
        "• **Class Action Waiver**: Prevents users/employees from joining together in a single lawsuit.\n"
        "• **Location/Cost**: Arbitration fees can be high if venue is set far away.\n"
        "• **Opt-out Rights**: Check if the agreement allows an opt-out within 30 days of signing.",
        [
            "What is unilateral change?",
            "What is auto renewal?",
            "What is governing law?",
        ],
    ),
    (
        ["auto renewal", "automatic renewal", "recurring fee", "cancel subscription"],
        "An **Auto-Renewal Clause** automatically extends a contract or subscription at the end of the term unless canceled in advance. Watch for:\n\n"
        "• **Notice Window**: Short cancellation windows (e.g. must give 60 days notice before renewal).\n"
        "• **Price Escalation**: Automatic price increases upon renewal.\n"
        "• **Cancellation Friction**: Requirement to cancel via certified mail or phone call rather than online.",
        [
            "What is a refund policy clause?",
            "What is unilateral change?",
            "What are payment terms?",
        ],
    ),
    (
        ["ip assignment", "intellectual property", "who owns code", "work for hire"],
        "An **IP Assignment Clause** transfers ownership of inventions, software, or creative work. Watch out for:\n\n"
        "• **Moonlighting / Side Projects**: Overbroad clauses claiming ownership of projects created in your personal free time.\n"
        "• **Pre-existing IP**: Explicitly carve out and list any pre-existing code, tools, or ideas you owned before signing.",
        [
            "What is a non-compete?",
            "What are payment terms?",
            "What is a confidentiality clause?",
        ],
    ),
    (
        ["termination for convenience", "terminate anytime", "early termination"],
        "**Termination for Convenience** allows a party to end the contract without needing to prove any breach or fault. Considerations:\n\n"
        "• **Notice Period**: Ensure sufficient notice (e.g. 30 days) to adjust or find replacement work.\n"
        "• **Work Done**: Guarantee payment for all work completed up to the termination date.",
        [
            "What is an indemnification clause?",
            "What is a late fee clause?",
            "How do I analyze a contract?",
        ],
    ),
]

DEFAULT_RESPONSE = (
    "I am the **PlainClause Legal AI Assistant**. I can help explain common contract terms, "
    "identify dangerous red flags, and guide your document reviews.\n\n"
    "**Try asking about:**\n"
    "• *Non-compete clauses & IP assignment*\n"
    "• *Lease security deposit traps & entry rights*\n"
    "• *Indemnification & liability caps*\n"
    "• *Mandatory arbitration & class action waivers*\n"
    "• *Auto-renewal & cancellation terms*"
)

DEFAULT_SUGGESTIONS = [
    "What is a non-compete clause?",
    "How does a security deposit clause work?",
    "What is indemnification?",
    "What is mandatory arbitration?",
    "What should I watch for in payment terms?",
]


def answer_query(query: str) -> Dict[str, Any]:
    """Process a user query and return an answer with suggested follow-up questions."""
    clean_query = query.strip().lower()
    if not clean_query:
        return {"reply": DEFAULT_RESPONSE, "suggested_questions": DEFAULT_SUGGESTIONS}

    for keywords, response_text, suggestions in KNOWLEDGE_BASE:
        for kw in keywords:
            if re.search(r"\b" + re.escape(kw) + r"\b", clean_query, re.IGNORECASE):
                return {"reply": response_text, "suggested_questions": suggestions}

    # Partial keyword matching fallback
    for keywords, response_text, suggestions in KNOWLEDGE_BASE:
        if any(kw in clean_query for kw in keywords):
            return {"reply": response_text, "suggested_questions": suggestions}

    # General help fallback
    return {
        "reply": (
            f"I reviewed your question regarding *'{query}'*. While PlainClause focuses on "
            "pattern-based clause detection in contracts, here are key rules of thumb for reviewing legal documents:\n\n"
            "1. **Check Obligations**: Look for clear definitions of scope, pay, and deadlines.\n"
            "2. **Identify Asymmetries**: Ensure rights to terminate, modify, or enforce terms are mutual.\n"
            "3. **Watch Restrictions**: Be cautious of non-competes, unlimited liability, and strict deposit penalties.\n\n"
            "You can paste your document into the **Document Analysis** tab to run a full clause-by-clause risk report!"
        ),
        "suggested_questions": DEFAULT_SUGGESTIONS,
    }
