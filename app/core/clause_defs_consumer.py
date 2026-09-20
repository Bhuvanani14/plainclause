"""Cancellation, audit, publicity and compliance provisions."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import (
    GROUP_LEGAL,
    GROUP_RIGHTS,
    ClauseType,
)

OPERATIONAL_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="cancellation",
        label="Cancellation rights",
        group=GROUP_LEGAL,
        summary="How you end an ongoing service or subscription.",
        base_severity=4,
        patterns=(
            r"cancel(l)?ation (right|period|policy|fee)",
            r"cooling-?off",
            r"may cancel .{0,30}(by|upon) (giving )?notice",
            r"notice of cancellation",
        ),
        keywords=("cancel", "cancellation", "cooling-off"),
        why_it_matters=(
            "Complicated cancellation steps are the main reason people keep paying for things "
            "they no longer want."
        ),
        watch_for=(
            "Cancellation only by phone or recorded post",
            "A notice period longer than the billing cycle",
            "Exit fees or forfeiture of amounts already paid",
        ),
        negotiation_tip=(
            "Ask for cancellation by the same channel you subscribed through, effective from the "
            "end of the current billing period, with written confirmation."
        ),
        expected_in=("terms_of_service", "services", "general"),
    ),
    ClauseType(
        id="audit_rights",
        label="Audit and inspection rights",
        group=GROUP_LEGAL,
        summary="Allows one side to inspect your records or premises.",
        base_severity=4,
        patterns=(
            r"\baudit\b",
            r"right to inspect .{0,25}(records|books|premises|systems)",
            r"books and records",
            r"inspect .{0,20}upon .{0,15}notice",
            r"(retain|maintain) .{0,25}records for",
        ),
        keywords=("audit", "inspect", "records", "books"),
        why_it_matters=(
            "Audit rights create real work and can expose confidential information about your "
            "other clients if the scope is not tightly drawn."
        ),
        watch_for=(
            "Unlimited audits at your cost and at any time",
            "Access to records about your other customers",
            "No notice period or reasonable-hours limit",
        ),
        negotiation_tip=(
            "Ask for audits only on reasonable notice, during business hours, limited to the "
            "relevant records, at the auditor's cost, and no more than once a year."
        ),
        expected_in=("services", "partnership", "general"),
    ),
    ClauseType(
        id="publicity",
        label="Publicity and use of your name",
        group=GROUP_RIGHTS,
        summary="Allows the other side to use your name, logo or case study.",
        base_severity=3,
        patterns=(
            r"(may )?use .{0,25}(your )?(name|logo|trademark) .{0,25}(marketing|promotional)",
            r"publicity .{0,25}(right|consent)",
            r"case study",
            r"reference .{0,20}customer",
        ),
        keywords=("publicity", "logo", "name", "marketing"),
        why_it_matters=(
            "Being named as a customer can reveal commercial relationships you would rather keep "
            "private, particularly when a client list is competitive information."
        ),
        watch_for=(
            "Unlimited promotional use without approval",
            "Use of your logo in a way that implies endorsement",
            "No right to withdraw consent later",
        ),
        negotiation_tip=(
            "Ask for each use to need your prior written approval, and for a right to withdraw "
            "consent on reasonable notice."
        ),
        expected_in=("services", "partnership", "general"),
    ),
    ClauseType(
        id="feedback_grant",
        label="Feedback licence",
        group=GROUP_RIGHTS,
        summary="Takes ownership or a licence over ideas you suggest.",
        base_severity=4,
        patterns=(
            r"feedback .{0,30}(grant|licen[cs]e|assign|property)",
            r"you (hereby )?(grant|assign) .{0,25}(feedback|suggestions)",
            r"free of (any )?charge .{0,25}(suggestions|feedback)",
            r"waive .{0,25}rights .{0,25}(feedback|suggestions)",
        ),
        keywords=("feedback", "suggestions", "ideas"),
        why_it_matters=(
            "If you suggest an improvement that turns out to be valuable, this clause can hand the "
            "idea over for nothing and stop you claiming credit for it."
        ),
        watch_for=(
            "Assignment of feedback with no compensation at all",
            "Wording wide enough to cover a new product idea you described",
            "No record of what was actually submitted",
        ),
        negotiation_tip=(
            "Ask for the licence to be limited to using the feedback to improve the existing "
            "service, and exclude any new product idea or invention."
        ),
        expected_in=("terms_of_service", "general"),
    ),
    ClauseType(
        id="scope_of_services",
        label="Scope of work",
        group=GROUP_LEGAL,
        summary="Defines exactly what is being delivered.",
        base_severity=3,
        patterns=(
            r"scope of (work|services|supply)",
            r"statement of work",
            r"deliverab(le|les)",
            r"specification .{0,25}set out in (schedule|annex|exhibit)",
            r"time and materials",
        ),
        keywords=("scope", "deliverables", "specification", "schedule"),
        why_it_matters=(
            "A vague scope is the most common cause of disputes on services contracts, because "
            "'reasonable additional work' can expand without limit and without extra payment."
        ),
        watch_for=(
            "Open-ended duties such as 'and other tasks as required'",
            "Deliverables described only by reference to a document you have not seen",
            "A change process with no right to adjust fees",
        ),
        negotiation_tip=(
            "Ask for a written list of deliverables with acceptance criteria, and for any change "
            "in scope to need written agreement with a fee and timeline adjustment."
        ),
        expected_in=("services", "general"),
    ),
    ClauseType(
        id="third_party_beneficiary",
        label="Third party rights",
        group=GROUP_LEGAL,
        summary="Says whether anyone outside the agreement can enforce it.",
        base_severity=3,
        patterns=(
            r"third-?party benefic",
            r"no third part(y|ies) .{0,25}(right|benefit)",
            r"contracts? \(rights of third parties\)",
            r"person who is not a party .{0,25}enforce",
        ),
        keywords=("third party", "beneficiary", "enforce"),
        why_it_matters=(
            "Excluding third party rights can stop a group company or an individual beneficiary "
            "from enforcing a promise that was made for their benefit."
        ),
        watch_for=(
            "Rights excluded for affiliates who depend on the agreement",
            "Exclusions that also block your own group companies",
        ),
        negotiation_tip=(
            "Ask for any affiliate or beneficiary who relies on the agreement to be named "
            "expressly so the exclusion does not undercut them."
        ),
        expected_in=("services", "partnership", "general"),
    ),
    ClauseType(
        id="insurance",
        label="Insurance requirements",
        group=GROUP_LEGAL,
        summary="Requires one side to hold and prove insurance cover.",
        base_severity=3,
        patterns=(
            r"\binsur(ance|ed|er)\b",
            r"maintain .{0,25}(professional indemnity|public liability|insurance)",
            r"certificate of insurance",
            r"policy of insurance",
        ),
        keywords=("insurance", "indemnity", "policy", "cover"),
        why_it_matters=(
            "Insurance is only useful if the cover is wide enough and the insurer still exists "
            "when a claim is made, which is why the limits and exclusions matter."
        ),
        watch_for=(
            "Required cover far above what is reasonable for the contract value",
            "No obligation to provide evidence of cover",
            "Cover that excludes the very risk the contract creates",
        ),
        negotiation_tip=(
            "Ask for limits proportionate to the contract value, evidence of cover on request, "
            "and notice if a policy lapses or is cancelled."
        ),
        expected_in=("services", "lease", "general"),
    ),
    ClauseType(
        id="compliance",
        label="Legal compliance promises",
        group=GROUP_LEGAL,
        summary="Promises that each side will follow applicable laws.",
        base_severity=3,
        patterns=(
            r"comply with all applicable (laws|regulations)",
            r"anti-?bribery|anti-?corruption",
            r"(economic )?sanctions",
            r"modern slavery",
            r"export control",
        ),
        keywords=("compliance", "laws", "sanctions", "bribery"),
        why_it_matters=(
            "A broad compliance promise can be breached by a change in the law far outside your "
            "control, and sanctions wording can be used to suspend payment quickly."
        ),
        watch_for=(
            "Compliance promises covering laws that apply only to the other side",
            "Suspension rights triggered by the other side's own assessment",
            "No cure period before a breach counts",
        ),
        negotiation_tip=(
            "Ask for the promise to cover laws each side is actually subject to, and for any "
            "suspension right to need written reasons and a cure period."
        ),
        expected_in=("services", "partnership", "general"),
    ),
)
