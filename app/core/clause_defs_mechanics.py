"""Contract mechanics provisions: set-off, early repayment and outside work."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import GROUP_MONEY, GROUP_RIGHTS, ClauseType

MECHANICS_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="set_off",
        label="Right of set-off",
        group=GROUP_MONEY,
        summary="Allows one side to net off money it thinks it is owed.",
        base_severity=5,
        patterns=(
            r"set ?-?off",
            r"right to (deduct|withhold) .{0,30}(sums|amounts)",
            r"may withhold (payment|any amount)",
            r"without prejudice to .{0,25}other rights",
        ),
        keywords=("set-off", "withhold", "net off"),
        why_it_matters=(
            "A set-off right lets the other side hold back money it claims you owe without "
            "waiting for anyone to agree that you owe it."
        ),
        watch_for=(
            "Set-off against sums that are not genuinely disputed",
            "Set-off applied across unrelated contracts",
            "No requirement to explain or evidence the deduction",
        ),
        negotiation_tip=(
            "Ask for set-off to be limited to undisputed, liquidated sums, with a written "
            "statement of the amount and reason, and no set-off across other agreements."
        ),
        expected_in=("loan", "services", "general"),
    ),
    ClauseType(
        id="early_repayment",
        label="Early repayment",
        group=GROUP_MONEY,
        summary="Whether you can pay off a debt early, and what it costs.",
        base_severity=5,
        patterns=(
            r"early (repayment|settlement|redemption)",
            r"prepay(ment)? (penalty|fee|charge)",
            r"(redeem|settle) .{0,25}in full .{0,25}(early|before)",
            r"early settlement (figure|amount)",
        ),
        keywords=("repayment", "prepayment", "settlement", "redeem"),
        why_it_matters=(
            "A prepayment penalty can make clearing a debt early more expensive than letting it "
            "run, which is often the opposite of what people expect."
        ),
        watch_for=(
            "Penalties calculated as a number of months of interest",
            "Settlement figures only available by phone",
            "Charges applied even when you are refinancing with the same lender",
        ),
        negotiation_tip=(
            "Ask for the settlement calculation to be written into the agreement, any penalty to "
            "be capped and to reduce over time, and a written figure on request."
        ),
        expected_in=("loan",),
    ),
    ClauseType(
        id="conflict_of_interest",
        label="Outside work and conflicts",
        group=GROUP_RIGHTS,
        summary="Controls what else you may do alongside the engagement.",
        base_severity=4,
        patterns=(
            r"conflict of interest",
            r"(prior )?written (consent|approval) .{0,25}outside (work|employment)",
            r"not .{0,25}engage in any other (business|employment)",
            r"full-?time and attention",
            r"devote .{0,25}(full|whole) time",
        ),
        keywords=("conflict", "outside", "exclusive", "attention"),
        why_it_matters=(
            "A broad full-time-and-attention or outside-work ban can stop you taking on any "
            "other work, even when there is no real conflict."
        ),
        watch_for=(
            "A ban on any other work rather than on conflicting work",
            "Approval that can be refused with no reason",
            "The duty continuing after hours without limit",
        ),
        negotiation_tip=(
            "Ask for the restriction to cover only genuinely competing activity, and for written "
            "approval of unrelated outside work not to be unreasonably withheld."
        ),
        expected_in=("employment", "services"),
    ),
)
