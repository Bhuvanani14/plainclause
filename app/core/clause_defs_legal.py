"""Dispute-resolution and warranty provisions."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import (
    GROUP_LEGAL,
    GROUP_MONEY,
    GROUP_RIGHTS,
    ClauseType,
)

LEGAL_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="arbitration",
        label="Arbitration agreement",
        group=GROUP_LEGAL,
        summary="Sends disputes to a private arbitrator instead of a court.",
        base_severity=7,
        patterns=(
            r"arbitrat(ion|or|ed)",
            r"arbitral tribunal",
            r"binding arbitration",
            r"dispute .{0,30}resolved by (an )?arbitr",
            r"rules of the .{0,25}arbitration",
        ),
        keywords=("arbitration", "arbitrator", "tribunal"),
        why_it_matters=(
            "Arbitration can be efficient for large organisations, but it usually means you pay "
            "your own costs with no appeal, no public hearing and a decision that is very hard "
            "to overturn."
        ),
        watch_for=(
            "Arbitration you must start hundreds of miles away",
            "Fees that make a small claim pointless to pursue",
            "The other side choosing the arbitrator or the rules",
            "No carve-out for small claims court or urgent injunctions",
        ),
        negotiation_tip=(
            "Ask to keep the right to use a small claims court or tribunal, for the venue to be "
            "near you, for costs to follow the same rules as a court, and for both sides to have "
            "the same appeal rights."
        ),
        expected_in=("terms_of_service", "services", "general"),
    ),
    ClauseType(
        id="class_action_waiver",
        label="Class action waiver",
        group=GROUP_LEGAL,
        summary="Stops you joining with others to bring a claim together.",
        base_severity=8,
        patterns=(
            r"class action",
            r"class arbitration",
            r"waive .{0,40}right to (participate in|join) .{0,20}(class|collective)",
            r"consolidate .{0,30}claims .{0,20}shall not",
        ),
        keywords=("class", "collective", "consolidate", "waive"),
        why_it_matters=(
            "A waiver means a wrong affecting thousands of people can only be challenged one "
            "person at a time, which is impractical for small amounts and rarely worth pursuing."
        ),
        watch_for=(
            "A waiver coupled with arbitration and buried in a long policy",
            "No carve-out for claims that cannot lawfully be waived",
            "Wording that also blocks your regulator or a public authority",
        ),
        negotiation_tip=(
            "Ask for the waiver to be removed, or at least to exclude claims where a group remedy "
            "is the only practical route, and to be clearly flagged in the summary."
        ),
        expected_in=("terms_of_service",),
    ),
    ClauseType(
        id="jury_waiver",
        label="Jury trial waiver",
        group=GROUP_LEGAL,
        summary="Gives up the right to have a jury decide a dispute.",
        base_severity=6,
        patterns=(
            r"waive .{0,30}jury",
            r"trial by jury",
            r"knowingly and voluntarily waiv",
            r"each party waives .{0,30}jury",
        ),
        keywords=("jury", "waive", "trial"),
        why_it_matters=(
            "A jury can be more sympathetic to an individual than a judge, and the waiver is "
            "often buried in closing boilerplate where nobody notices it."
        ),
        watch_for=(
            "A waiver that does not say who benefits from it",
            "A waiver applied to claims where it may not be enforceable",
        ),
        negotiation_tip=(
            "Ask for the waiver to be removed, or at least to be mutual and explicitly flagged in "
            "the summary so nobody signs it by accident."
        ),
        expected_in=("terms_of_service", "services", "general"),
    ),
    ClauseType(
        id="governing_law",
        label="Governing law",
        group=GROUP_LEGAL,
        summary="Chooses which country's or state's law applies.",
        base_severity=3,
        patterns=(
            r"governed by (and construed in accordance with )?the laws of",
            r"governing law",
            r"construed in accordance with .{0,30}laws",
            r"without regard to .{0,25}conflict of laws",
        ),
        keywords=("governed", "laws", "construed"),
        why_it_matters=(
            "The governing law decides which rules and protections apply to your agreement, and "
            "consumer protections where you live may not travel with you."
        ),
        watch_for=(
            "A jurisdiction where you have no practical access to courts",
            "A jurisdiction chosen because it gives consumers fewer protections",
            "Governing law and the dispute venue pointing to different places",
        ),
        negotiation_tip=(
            "Ask for the law of the place where you live or where the service is delivered, and "
            "for any mandatory local protections to be preserved."
        ),
        expected_in=("terms_of_service", "services", "general"),
    ),
    ClauseType(
        id="jurisdiction_venue",
        label="Jurisdiction and venue",
        group=GROUP_LEGAL,
        summary="Chooses where a dispute must be heard.",
        base_severity=4,
        patterns=(
            r"exclusive jurisdiction",
            r"submit to the .{0,25}jurisdiction",
            r"venue (shall be|lies)",
            r"courts of .{0,30}shall have",
            r"irrevocably submit",
        ),
        keywords=("jurisdiction", "venue", "courts", "submit"),
        why_it_matters=(
            "A distant venue can make a valid claim worthless in practice, because travel and "
            "representation cost more than the dispute is worth."
        ),
        watch_for=(
            "'Exclusive jurisdiction' far from where you live",
            "A venue chosen purely for the other side's convenience",
            "Mandatory local consumer rights excluded",
        ),
        negotiation_tip=(
            "Ask for disputes to be heard where you live, or at minimum for you to keep the right "
            "to sue in your own courts."
        ),
        expected_in=("terms_of_service", "services", "general"),
    ),
    ClauseType(
        id="warranty_disclaimer",
        label="Warranty disclaimer",
        group=GROUP_RIGHTS,
        summary="Removes promises about quality, fitness or condition.",
        base_severity=5,
        patterns=(
            r"disclaims? .{0,25}warrant",
            r"no warrant(y|ies) of any kind",
            r'provided (on an )?"as is" basis',
            r"fitness for a particular purpose",
            r"merchantability",
            r"without warrant(y|ies) of any kind",
        ),
        keywords=("warranty", "as is", "merchantability", "fitness"),
        why_it_matters=(
            "A disclaimer removes the promise that the thing works or is fit for your purpose, "
            "which is usually the promise you relied on when you bought it."
        ),
        watch_for=(
            "Disclaimers that contradict a written specification or demo",
            "No remedy at all if the product does not work",
            "Disclaimers that override mandatory statutory rights",
        ),
        negotiation_tip=(
            "Ask for a warranty that matches what you were promised, and for warranties to be "
            "limited in time rather than removed entirely."
        ),
        expected_in=("terms_of_service", "loan", "general"),
    ),
    ClauseType(
        id="refund_policy",
        label="Refunds",
        group=GROUP_MONEY,
        summary="Whether you can get your money back, and when.",
        base_severity=5,
        patterns=(
            r"non-?refundable",
            r"no refunds?",
            r"refund(s)? (will|shall|may) (not )?be",
            r"eligib(le|ility) for a refund",
            r"all sales are final",
        ),
        keywords=("refund", "refundable", "final", "return"),
        why_it_matters=(
            "A no-refund rule means you carry all the risk if the service does not deliver what "
            "was described, and it can conflict with statutory cancellation rights."
        ),
        watch_for=(
            "'All sales final' with no service guarantee",
            "Refunds offered only as credit that expires",
            "Cancellation rights narrower than local consumer law allows",
        ),
        negotiation_tip=(
            "Ask for a refund if the service is not delivered as described, a pro-rata refund on "
            "cancellation, and confirmation that your statutory rights are unaffected."
        ),
        expected_in=("terms_of_service", "loan", "general"),
    ),
)
