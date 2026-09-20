"""Who is reading the document, and why that changes the review.

The same clause carries very different weight for different readers.  A
non-compete is background noise in a software licence but career-defining in an
employment contract; a security deposit clause matters enormously to a tenant
and barely at all to a software buyer.

Rather than one generic checklist, each persona selects the archetype to check
against, overrides the severity of specific clause types, and supplies the
wording for follow-up questions and the lawyer handover.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Mapping

OTHER_PERSONA_ID: Final = "other"
MIN_SEVERITY: Final = 0
MAX_SEVERITY: Final = 10


@dataclass(frozen=True, slots=True)
class Persona:
    """A reader profile that biases the whole review."""

    id: str
    label: str
    blurb: str
    preferred_archetype: str
    focus_types: tuple[str, ...] = ()
    severity_weights: Mapping[str, int] = field(default_factory=dict)
    intro: str = ""
    questions: tuple[str, ...] = ()
    documents_to_gather: tuple[str, ...] = ()


_PERSONA_LIST: tuple[Persona, ...] = (
    Persona(
        id="tenant",
        label="Tenant or flatmate",
        blurb="Renting a home and reviewing a lease or tenancy agreement.",
        preferred_archetype="lease",
        focus_types=(
            "security_deposit",
            "rent_increase",
            "maintenance_obligation",
            "subletting",
            "entry_rights",
            "auto_renewal",
            "termination_convenience",
            "late_fee",
        ),
        severity_weights={
            "security_deposit": 2,
            "rent_increase": 2,
            "entry_rights": 2,
            "subletting": 2,
            "maintenance_obligation": 2,
            "auto_renewal": 1,
            "late_fee": 1,
            "non_compete": -4,
            "non_solicitation": -4,
            "ip_assignment": -3,
        },
        intro=(
            "You are reviewing a tenancy document. The clauses that most often cost "
            "tenants money are the deposit, rent review, repair duties and the "
            "landlord's right of entry."
        ),
        questions=(
            "Who holds my deposit, and what must happen for it to be returned in full?",
            "How much notice must the landlord give before entering, and for what reasons?",
            "What repairs are my responsibility and which are the landlord's?",
            "Can the rent be increased during the fixed term, and by how much?",
            "What exactly must I do at the end of the tenancy to avoid a deduction?",
        ),
        documents_to_gather=(
            "The signed tenancy agreement and any addendum",
            "The inventory or condition report from move-in day",
            "Dated photos of the property at move-in and move-out",
            "Receipts for any repairs or works you paid for",
            "Proof of every rent payment made",
        ),
    ),
    Persona(
        id="employee",
        label="Employee or job applicant",
        blurb="Reviewing an employment contract, offer letter or restrictive covenant.",
        preferred_archetype="employment",
        focus_types=(
            "non_compete",
            "non_solicitation",
            "ip_assignment",
            "notice_period",
            "probation",
            "overtime_pay",
            "salary_deduction",
            "termination_convenience",
            "confidentiality",
            "background_check",
        ),
        severity_weights={
            "non_compete": 3,
            "non_solicitation": 2,
            "ip_assignment": 2,
            "probation": 1,
            "overtime_pay": 2,
            "salary_deduction": 3,
            "termination_convenience": 2,
            "background_check": 1,
            "security_deposit": -4,
            "rent_increase": -4,
        },
        intro=(
            "You are reviewing an employment document. The clauses most likely to "
            "affect your career and your pay are the restrictive covenants, the "
            "intellectual property assignment and the notice and probation terms."
        ),
        questions=(
            "How long does the non-compete last, and what geographic and industry scope does it cover?",
            "Do I keep ownership of work I create outside working hours and outside my job duties?",
            "What notice must each side give, and can I be dismissed without notice?",
            "Is overtime paid, time off in lieu, or unpaid?",
            "Can the employer deduct money from my pay, and in what circumstances?",
        ),
        documents_to_gather=(
            "The full contract and any schedule or annex",
            "The offer letter and any email variation to the terms",
            "The employee handbook or policy documents it refers to",
            "Any bonus, commission or share plan rules",
            "Your job description and any agreed scope changes",
        ),
    ),
    Persona(
        id="freelancer",
        label="Freelancer or small supplier",
        blurb="Reviewing a client contract, statement of work or master services agreement.",
        preferred_archetype="services",
        focus_types=(
            "payment_terms",
            "late_fee",
            "ip_assignment",
            "termination_convenience",
            "liability_cap",
            "indemnity",
            "non_compete",
            "exclusivity",
            "scope_of_services",
            "audit_rights",
        ),
        severity_weights={
            "payment_terms": 2,
            "late_fee": 2,
            "ip_assignment": 2,
            "termination_convenience": 2,
            "liability_cap": -1,
            "indemnity": 2,
            "exclusivity": 2,
            "scope_of_services": 2,
            "audit_rights": 1,
            "security_deposit": -4,
        },
        intro=(
            "You are reviewing a client-facing services document. The clauses that "
            "most often hurt suppliers are payment terms, the right to terminate for "
            "convenience, unpaid indemnities and broad intellectual property transfers."
        ),
        questions=(
            "When exactly is each invoice payable, and what happens if it is paid late?",
            "Can the client terminate without cause, and am I paid for work already done?",
            "What am I promising to indemnify the client for, and is that capped?",
            "Is my total liability capped at the contract value, or is it unlimited?",
            "What is expressly out of scope so I can charge for it separately?",
        ),
        documents_to_gather=(
            "The signed contract, statement of work and any change orders",
            "Your original quote or proposal and the client's acceptance",
            "All invoices issued and payment records received",
            "Written records of scope changes agreed by email",
            "Any purchase order or supplier onboarding terms",
        ),
    ),
    Persona(
        id="consumer",
        label="Consumer or app user",
        blurb="Reviewing terms of service, a subscription or a privacy policy.",
        preferred_archetype="terms_of_service",
        focus_types=(
            "arbitration",
            "class_action_waiver",
            "auto_renewal",
            "unilateral_change",
            "refund_policy",
            "data_sharing",
            "data_processing",
            "liability_cap",
            "cancellation",
            "jury_waiver",
        ),
        severity_weights={
            "arbitration": 3,
            "class_action_waiver": 3,
            "jury_waiver": 2,
            "auto_renewal": 2,
            "unilateral_change": 3,
            "data_sharing": 2,
            "refund_policy": 2,
            "cancellation": 1,
            "non_compete": -4,
        },
        intro=(
            "You are reviewing consumer-facing terms. The clauses with the biggest "
            "practical effect are how you can complain or sue, how the terms can be "
            "changed without your agreement, and how your data is shared."
        ),
        questions=(
            "If something goes wrong, must I use private arbitration instead of a court?",
            "Can I join others in a group claim if many users are affected?",
            "How much notice will I get before the terms change, and can I exit then?",
            "Does the subscription renew automatically, and how do I cancel it?",
            "Who do you share my personal data with, and can I refuse?",
        ),
        documents_to_gather=(
            "Screenshots of the terms you actually agreed to, with the date",
            "The sign-up confirmation and any renewal reminder emails",
            "Payment receipts or bank statements for the subscription",
            "Copies of support chats or complaints you have raised",
            "The privacy policy in force when you signed up",
        ),
    ),
    Persona(
        id="founder",
        label="Founder or business partner",
        blurb="Reviewing a partnership, shareholder, investor or joint venture document.",
        preferred_archetype="partnership",
        focus_types=(
            "ip_assignment",
            "exclusivity",
            "non_compete",
            "indemnity",
            "termination_breach",
            "unilateral_change",
            "assignment",
            "liability_cap",
        ),
        severity_weights={
            "ip_assignment": 3,
            "exclusivity": 3,
            "unilateral_change": 2,
            "assignment": 2,
            "termination_breach": 2,
            "non_compete": 1,
            "security_deposit": -4,
            "rent_increase": -4,
        },
        intro=(
            "You are reviewing a business or investment document. The clauses that "
            "most often decide who really controls the company are intellectual "
            "property ownership, exclusivity and the rights to change or exit."
        ),
        questions=(
            "Who owns the intellectual property created by the business, and can it be assigned away?",
            "Can the other side change the agreement or my rights without my consent?",
            "What triggers a forced exit, and at what valuation?",
            "What are my personal liabilities as opposed to the company's?",
            "Can my stake or rights be transferred to someone I have not agreed to?",
        ),
        documents_to_gather=(
            "The term sheet and the full definitive agreement",
            "The cap table and any side letters",
            "The company's constitutional documents",
            "Founder or shareholder agreements and vesting schedules",
            "Board minutes approving the transaction",
        ),
    ),
    Persona(
        id="buyer",
        label="Buyer or borrower",
        blurb="Reviewing a purchase, loan, credit or hire-purchase agreement.",
        preferred_archetype="loan",
        focus_types=(
            "interest",
            "payment_terms",
            "late_fee",
            "warranty_disclaimer",
            "liability_cap",
            "refund_policy",
            "cancellation",
            "security_deposit",
            "set_off",
        ),
        severity_weights={
            "interest": 2,
            "late_fee": 2,
            "warranty_disclaimer": 2,
            "set_off": 1,
            "refund_policy": 2,
            "non_compete": -4,
        },
        intro=(
            "You are reviewing a purchase or credit document. The clauses that most "
            "often cost money are the interest calculation, the fees, and the "
            "disclaimers of warranty that remove your right to complain about faults."
        ),
        questions=(
            "What is the total amount repayable, including all interest and fees?",
            "Can the interest rate or fees change, and by how much?",
            "What are my rights if the goods or service are faulty?",
            "If I repay early, is there a penalty?",
            "Can the lender take money from my account or set off other balances?",
        ),
        documents_to_gather=(
            "The full agreement including the schedule of charges",
            "The key facts or pre-contract summary document",
            "Every statement showing payments and charges applied",
            "Correspondence about arrears, forbearance or variation",
            "Evidence of any insurance sold alongside the credit",
        ),
    ),
    Persona(
        id=OTHER_PERSONA_ID,
        label="Something else",
        blurb="A general review when the category above does not fit.",
        preferred_archetype="general",
        focus_types=(
            "liability_cap",
            "indemnity",
            "termination_convenience",
            "auto_renewal",
            "payment_terms",
            "confidentiality",
            "governing_law",
            "unilateral_change",
        ),
        severity_weights={},
        intro=(
            "You are reviewing a legal document without a specific persona selected, "
            "so PlainClause checks the general-purpose provision list."
        ),
        questions=(
            "What am I obliged to do, by when, and what happens if I cannot?",
            "What rights does the other side have that I do not?",
            "How does this agreement end, and what happens to what I have already paid?",
            "Which country's or state's law governs, and where would disputes be heard?",
            "What would a lawyer need from me to give me proper advice?",
        ),
        documents_to_gather=(
            "The complete signed document and every annex",
            "Any correspondence that varies the terms",
            "Proof of payments, notices or deliveries",
            "The other side's policy documents it refers to",
        ),
    ),
)

PERSONAS: Final[Mapping[str, Persona]] = {persona.id: persona for persona in _PERSONA_LIST}
PERSONA_IDS: Final[tuple[str, ...]] = tuple(persona.id for persona in _PERSONA_LIST)


def get_persona(persona_id: str) -> Persona:
    """Look up a persona, falling back to the general one."""
    return PERSONAS.get(persona_id) or PERSONAS[OTHER_PERSONA_ID]


def severity_weight(persona_id: str, clause_type: str) -> int:
    """How much this persona's concerns should shift a clause type's severity."""
    return get_persona(persona_id).severity_weights.get(clause_type, 0)


def clamp_severity(value: int) -> int:
    return max(MIN_SEVERITY, min(MAX_SEVERITY, value))


def jurisdiction_caution(jurisdiction: str) -> str:
    """A careful, honest note about jurisdiction — never a legal conclusion."""
    where = jurisdiction.strip()
    if not where:
        return (
            "No jurisdiction was given. Rules differ a great deal between countries and "
            "states, and many clauses that are enforceable in one place are not in another."
        )
    return (
        f"You noted {where} as the relevant jurisdiction. PlainClause does not verify local "
        "rules and cannot confirm whether a clause is enforceable there. Some protections "
        "in your area may override the contract whether or not it says so, so this point is "
        "worth confirming with a qualified professional."
    )