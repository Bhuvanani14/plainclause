"""Money and exit provisions: the clauses that most often cost people cash."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import (
    GROUP_EXIT,
    GROUP_MONEY,
    ClauseType,
)

MONEY_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="liability_cap",
        label="Limitation of liability",
        group=GROUP_MONEY,
        summary="Sets a ceiling on how much one side can ever have to pay the other.",
        base_severity=6,
        patterns=(
            r"limit(ation)? of liability",
            r"total liability",
            r"aggregate liability",
            r"shall not exceed",
            r"in no event shall",
            r"capped at",
            r"maximum liability",
        ),
        keywords=("cap", "liability", "exceed", "aggregate"),
        why_it_matters=(
            "A cap decides the most you can ever recover, or the most you can ever be asked "
            "to pay. A low cap can make a serious breach almost worthless to sue over."
        ),
        watch_for=(
            "A cap set at the fees paid, even where the loss is far larger",
            "The other side's own wrongdoing left out of the calculation",
            "Liability uncapped on your side but capped on theirs",
        ),
        negotiation_tip=(
            "Ask for the cap to be mutual, set at a meaningful multiple of the contract "
            "value, and for fraud, confidentiality breaches and intellectual property "
            "infringement to sit outside it."
        ),
        expected_in=("services", "terms_of_service", "loan", "general"),
    ),
    ClauseType(
        id="indemnity",
        label="Indemnity",
        group=GROUP_MONEY,
        summary="A promise to cover the other side's losses and legal costs.",
        base_severity=7,
        patterns=(
            r"indemnif",
            r"hold harmless",
            r"defend .{0,25}against",
            r"reimburse .{0,25}for (any|all)",
            r"keep .{0,20}indemnified",
        ),
        keywords=("indemnify", "indemnity", "harmless", "reimburse"),
        why_it_matters=(
            "An indemnity is close to a blank cheque for someone else's losses. It can "
            "require you to pay legal costs even when the claim is settled with no finding "
            "against you."
        ),
        watch_for=(
            "Indemnities you give that are not matched by one you receive",
            "Indemnities covering the other side's own negligence",
            "No cap, and no duty on them to defend the claim properly",
        ),
        negotiation_tip=(
            "Make it mutual, limit it to third-party claims actually caused by your breach, "
            "exclude their own fault, cap it, and require prompt notice before it applies."
        ),
        expected_in=("services", "partnership", "lease", "general"),
    ),
    ClauseType(
        id="payment_terms",
        label="Payment terms",
        group=GROUP_MONEY,
        summary="When money is due, how it is invoiced and what it covers.",
        base_severity=4,
        patterns=(
            r"payable within\b",
            r"payment (shall|will) be made",
            r"due within \b(\d{1,3})\s?days",
            r"invoice .{0,30}(within|upon|after)",
            r"net \d{1,3}\b",
        ),
        keywords=("invoice", "payable", "payment", "due"),
        why_it_matters=(
            "Long payment terms quietly turn into an interest-free loan from you to the "
            "other side, and 'on completion' wording can postpone payment indefinitely."
        ),
        watch_for=(
            "Payment conditional on the other side being satisfied with the work",
            "Ninety-day or open-ended terms on a small contract",
            "No rule about who pays transfer fees and bank charges",
        ),
        negotiation_tip=(
            "Ask for payment within fourteen to thirty days of a valid invoice, a deposit "
            "up front, and a clear rule on who pays transaction fees."
        ),
        expected_in=("services", "loan", "general"),
    ),
    ClauseType(
        id="late_fee",
        label="Late payment charges",
        group=GROUP_MONEY,
        summary="Extra money owed when a payment is late.",
        base_severity=5,
        patterns=(
            r"late (fee|charge|payment (fee|charge))",
            r"(interest|charge) at the rate of .{0,20}%",
            r"past due",
            r"administrative (fee|charge) .{0,20}(late|overdue)",
            r"penalt(y|ies) (of|for) ",
        ),
        keywords=("late", "overdue", "penalty", "charge"),
        why_it_matters=(
            "Late charges compound quickly, and a rate quoted per month can be far larger "
            "than it first appears."
        ),
        watch_for=(
            "A monthly figure that is really an annual rate in disguise",
            "Fixed administration fees stacked on top of interest",
            "Charges applied while you are disputing the invoice in good faith",
        ),
        negotiation_tip=(
            "Ask for a single rate expressed per year, a short grace period, and no charge "
            "while an invoice is disputed in writing and within time."
        ),
        expected_in=("loan", "services", "lease", "terms_of_service"),
    ),
    ClauseType(
        id="interest",
        label="Interest",
        group=GROUP_MONEY,
        summary="The cost of borrowing, and how it is calculated or changed.",
        base_severity=6,
        patterns=(
            r"\binterest\b.{0,40}\b\d{1,2}(\.\d+)?\s?%",
            r"\b\d{1,2}(\.\d+)?\s?%\s?(per annum|p\.?a\.?|annually)",
            r"annual percentage rate",
            r"rate of interest",
            r"variable (rate|interest)",
        ),
        keywords=("interest", "rate", "per annum", "apr"),
        why_it_matters=(
            "This clause fixes the real cost of the deal. A variable rate means the total "
            "you repay is not the total you were quoted."
        ),
        watch_for=(
            "A rate that moves with an index you cannot see or control",
            "Interest calculated daily rather than monthly or annually",
            "Interest continuing to run after you have repaid the principal",
        ),
        negotiation_tip=(
            "Ask for the total repayable in figures, written notice plus a cap before any "
            "rate change, and a worked example of how interest is calculated."
        ),
        expected_in=("loan", "general"),
    ),
    ClauseType(
        id="price_increase",
        label="Price or fee changes",
        group=GROUP_MONEY,
        summary="Allows the other side to raise what you pay.",
        base_severity=5,
        patterns=(
            r"(increase|raise|adjust) .{0,25}(fee|fees|price|prices|charge|charges|rate)",
            r"(fee|price)s? .{0,20}may (be )?(increase|change|vary)",
            r"subject to (an )?annual (increase|uplift|adjustment)",
            r"uplift",
        ),
        keywords=("increase", "adjust", "uplift", "fee"),
        why_it_matters=(
            "An open right to raise prices means the deal you agreed is not the deal you "
            "will be paying for in twelve months."
        ),
        watch_for=(
            "Increases at their discretion with no ceiling",
            "Increases tied to an index that is unpublished or easily gamed",
            "A price rise with no matching right for you to walk away",
        ),
        negotiation_tip=(
            "Ask for a fixed price for an initial period, a stated cap on later rises, and "
            "the right to leave without penalty if the increase exceeds that cap."
        ),
        expected_in=("terms_of_service", "services", "lease"),
    ),
    ClauseType(
        id="liquidated_damages",
        label="Liquidated damages or penalty",
        group=GROUP_MONEY,
        summary="A fixed sum payable when something goes wrong.",
        base_severity=6,
        patterns=(
            r"liquidated damages",
            r"agreed damages",
            r"penalt(y|ies) (of|in the amount)",
            r"as a genuine pre-?estimate of loss",
        ),
        keywords=("liquidated", "damages", "penalty"),
        why_it_matters=(
            "A fixed sum avoids arguing about loss, but it can be far more than the real "
            "damage and may be triggered by something outside your control."
        ),
        watch_for=(
            "A daily rate with no overall ceiling",
            "Triggers based on delays you cannot influence, such as permits",
            "The same event producing damages and termination at once",
        ),
        negotiation_tip=(
            "Ask for an overall cap on total damages, an exclusion for delays caused by the "
            "other side or by events outside your control, and a grace period before it starts."
        ),
        expected_in=("services", "lease", "general"),
    ),
    ClauseType(
        id="termination_convenience",
        label="Termination for convenience",
        group=GROUP_EXIT,
        summary="Lets one side walk away for any reason, or no reason at all.",
        base_severity=6,
        patterns=(
            r"terminate .{0,40}for convenience",
            r"terminate (this agreement|these terms)? ?at any time",
            r"terminate .{0,30}without cause",
            r"without assigning any reason",
            r"sole discretion .{0,30}terminat",
        ),
        keywords=("terminate", "cancellation", "without cause", "convenience"),
        why_it_matters=(
            "If the other side can leave at any time but you cannot, you carry all the risk "
            "of the arrangement while holding none of the control."
        ),
        watch_for=(
            "Termination without cause on short notice and no payment for work done",
            "A one-sided exit right beside a long lock-in on your side",
            "No obligation to pay for costs you have already committed",
        ),
        negotiation_tip=(
            "Ask for a mutual right with defined notice, payment for all completed work and "
            "committed costs, and a stated notice window such as thirty days."
        ),
        expected_in=("services", "terms_of_service", "employment", "general"),
    ),
    ClauseType(
        id="termination_breach",
        label="Termination for breach",
        group=GROUP_EXIT,
        summary="Ends the agreement when one side breaks a serious term.",
        base_severity=4,
        patterns=(
            r"material(ly)? breach",
            r"terminate .{0,40}(breach|default)",
            r"in the event of (a )?(breach|default)",
            r"cure period",
            r"fails to remedy",
        ),
        keywords=("breach", "default", "remedy", "cure"),
        why_it_matters=(
            "The notice and cure period decide whether a small misunderstanding can end the "
            "whole relationship immediately."
        ),
        watch_for=(
            "Immediate termination with no chance to fix the problem",
            "One side deciding unilaterally whether a breach is 'material'",
        ),
        negotiation_tip=(
            "Ask for written notice of the breach and at least fourteen to thirty days to "
            "put it right before termination can take effect."
        ),
        expected_in=("services", "lease", "partnership", "general"),
    ),
    ClauseType(
        id="auto_renewal",
        label="Automatic renewal",
        group=GROUP_EXIT,
        summary="Rolls the agreement over unless you cancel in time.",
        base_severity=6,
        patterns=(
            r"automatically renew",
            r"auto-?renew",
            r"renew .{0,30}for (a )?(further|successive|additional) (term|period|year)",
            r"evergreen",
            r"shall be extended automatically",
        ),
        keywords=("renew", "renewal", "automatic", "successive"),
        why_it_matters=(
            "Auto-renewal traps people into another full term because the cancellation "
            "window is easy to miss and often closes months before the end date."
        ),
        watch_for=(
            "A long renewal term with a narrow cancellation window",
            "A price increase applied on renewal without a fresh agreement",
            "Cancellation accepted only by one awkward method such as recorded post",
        ),
        negotiation_tip=(
            "Ask for a written reminder before the window opens, a month-to-month option, "
            "and cancellation by ordinary email with confirmation."
        ),
        expected_in=("terms_of_service", "services", "lease", "general"),
    ),
    ClauseType(
        id="notice_period",
        label="Notice period",
        group=GROUP_EXIT,
        summary="How much warning each side must give before ending the arrangement.",
        base_severity=4,
        patterns=(
            r"notice period",
            r"upon .{0,20}\b(\d{1,3})\s?(day|week|month)s?.{0,15}notice",
            r"written notice of (at least )?\b(\d{1,3})",
            r"give (at least )?\b(\d{1,3})\s?(day|week|month)s? notice",
        ),
        keywords=("notice", "days", "weeks", "months"),
        why_it_matters=(
            "Short notice against you means little warning of lost income or lost housing; "
            "long notice against you can lock you in place."
        ),
        watch_for=(
            "Notice periods that are longer for you than for them",
            "Notice by a method you cannot prove, such as a phone call",
            "A start date for notice that is hard to verify",
        ),
        negotiation_tip=(
            "Make the notice period equal on both sides, require it in writing, and state "
            "exactly when the clock starts — for example the day after delivery."
        ),
        expected_in=("employment", "lease", "services", "general"),
    ),
    ClauseType(
        id="force_majeure",
        label="Force majeure",
        group=GROUP_EXIT,
        summary="Excuses performance when something outside anyone's control happens.",
        base_severity=3,
        patterns=(
            r"force majeure",
            r"acts? of god",
            r"beyond .{0,25}reasonable control",
            r"epidemic|pandemic|lockdown",
        ),
        keywords=("majeure", "unforeseeable", "control"),
        why_it_matters=(
            "A narrow force majeure clause leaves you in breach for events you could not "
            "prevent; a very wide one lets the other side pause the contract and stop paying."
        ),
        watch_for=(
            "A clause wide enough to cover ordinary financial difficulty",
            "Suspension of payment obligations without a right for you to exit",
            "No long-stop date, so the pause can last forever",
        ),
        negotiation_tip=(
            "Ask for a list of covered events, exclusion of financial hardship, and a right "
            "to terminate and settle up if the event continues beyond a set period."
        ),
        expected_in=("services", "lease", "general"),
    ),
)
