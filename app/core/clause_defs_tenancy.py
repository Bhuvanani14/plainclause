"""Tenancy money provisions: deposits and rent review."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import GROUP_MONEY, ClauseType

TENANCY_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="security_deposit",
        label="Deposit",
        group=GROUP_MONEY,
        summary="Money held up front, and the rules for getting it back.",
        base_severity=6,
        patterns=(
            r"security deposit",
            r"deposit .{0,25}(held|retained|refund)",
            r"forfeit .{0,25}deposit",
            r"deduct .{0,25}from the deposit",
            r"\bbond\b",
        ),
        keywords=("deposit", "bond", "deduction", "forfeit"),
        why_it_matters=(
            "The deposit is usually the largest sum you have at risk. Vague deduction wording "
            "is the most common reason tenants lose money at the end of a tenancy."
        ),
        watch_for=(
            "Deductions for any reason, or for general wear and tear",
            "No deadline for returning the money after you move out",
            "No requirement for an itemised statement or receipts",
            "Automatic forfeiture for breaking any term, however minor",
        ),
        negotiation_tip=(
            "Ask for a stated return deadline, an itemised statement with receipts for every "
            "deduction, no deduction for fair wear and tear, and an inventory signed by both "
            "sides at move-in."
        ),
        expected_in=("lease",),
    ),
    ClauseType(
        id="rent_increase",
        label="Rent increase",
        group=GROUP_MONEY,
        summary="How and when the rent can go up.",
        base_severity=5,
        patterns=(
            r"rent .{0,25}(increase|review|escalat|adjust)",
            r"(increase|review) .{0,20}rent",
            r"annual (rent )?(review|increase|escalation)",
            r"market rent",
        ),
        keywords=("rent", "increase", "review", "escalation"),
        why_it_matters=(
            "A rent review can raise your biggest regular cost, and market-rent wording leaves "
            "the amount to be argued about rather than agreed."
        ),
        watch_for=(
            "Increases during a fixed term that the clause allows",
            "Unlimited increases, or increases set by the landlord alone",
            "An undefined market rent with no fallback if you disagree",
        ),
        negotiation_tip=(
            "Ask for a fixed rent for the whole term, then rises capped at a stated percentage "
            "or a published index, with notice before they take effect."
        ),
        expected_in=("lease",),
    ),
)
