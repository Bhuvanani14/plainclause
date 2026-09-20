"""Employment provisions: hours, probation, pay deductions and screening."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import GROUP_MONEY, GROUP_PEOPLE, ClauseType

EMPLOYMENT_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="overtime_pay",
        label="Overtime and extra hours",
        group=GROUP_MONEY,
        summary="What you are paid for hours beyond your normal schedule.",
        base_severity=5,
        patterns=(
            r"overtime",
            r"additional hours",
            r"time off in lieu",
            r"(toil|flexi-?time)",
            r"no additional payment .{0,25}(hours|work)",
            r"exempt .{0,20}overtime",
        ),
        keywords=("overtime", "additional", "hours", "lieu"),
        why_it_matters=(
            "Unpaid overtime can quietly cut your real hourly rate, and a salary described as "
            "covering all hours necessary can mean unlimited unpaid work."
        ),
        watch_for=(
            "A salary expressed as covering any hours required",
            "Time off in lieu with no expiry or scheduling commitment",
            "No limit on the number of extra hours expected",
        ),
        negotiation_tip=(
            "Ask how extra hours are recorded, whether they are paid or banked, and for a clear "
            "limit beyond which extra pay applies."
        ),
        expected_in=("employment",),
    ),
    ClauseType(
        id="probation",
        label="Probationary period",
        group=GROUP_PEOPLE,
        summary="An initial period with weaker rights and shorter notice.",
        base_severity=4,
        patterns=(
            r"probation(ary)?",
            r"probationary period",
            r"initial (trial|review) period",
            r"(first|initial) .{0,20}(three|six|3|6) months",
            r"confirmation of employment",
        ),
        keywords=("probation", "trial", "confirmation"),
        why_it_matters=(
            "During probation you usually have shorter notice and fewer protections, and the "
            "period can sometimes be extended at will."
        ),
        watch_for=(
            "A long probation, such as twelve months",
            "Extendable at the employer's discretion with no limit",
            "Reduced benefits or no notice at all during probation",
        ),
        negotiation_tip=(
            "Ask for a defined probation length, a single extension at most, written reasons "
            "before any extension, and your normal notice to apply if they keep you on."
        ),
        expected_in=("employment",),
    ),
    ClauseType(
        id="salary_deduction",
        label="Deductions from pay",
        group=GROUP_MONEY,
        summary="Lets money be taken off what you are owed.",
        base_severity=7,
        patterns=(
            r"deduct .{0,30}(from )?(your )?(salary|wages|pay|remuneration)",
            r"set off .{0,30}against (salary|wages|pay)",
            r"withhold .{0,25}(payment|salary|wages)",
            r"authorise .{0,25}deduction",
        ),
        keywords=("deduct", "withhold", "wages", "salary"),
        why_it_matters=(
            "A broad deduction right means your pay can shrink for reasons you dispute, and in "
            "many places deductions require your written consent or another legal basis."
        ),
        watch_for=(
            "Deductions for losses or shortages with no evidence required",
            "Deductions made with no notice or chance to respond",
            "Set-off against final pay, including disputed sums",
        ),
        negotiation_tip=(
            "Ask for deductions to need your prior written agreement, notice of the amount and "
            "reason, and a chance to dispute it before money is taken."
        ),
        expected_in=("employment",),
    ),
    ClauseType(
        id="background_check",
        label="Background checks",
        group=GROUP_PEOPLE,
        summary="Consent to checks on your history or right to work.",
        base_severity=3,
        patterns=(
            r"background (check|screening)",
            r"criminal (record|conviction)",
            r"right to work (check|verification)",
            r"credit (check|reference)",
            r"reference(s)? check",
        ),
        keywords=("background", "screening", "criminal", "reference"),
        why_it_matters=(
            "Checks affect your privacy and can be a route to withdrawing an offer, so what is "
            "checked, when, and who sees the result all matter."
        ),
        watch_for=(
            "Open-ended consent to any background enquiry",
            "Checks after you have started, with no appeal route",
            "Credit checks irrelevant to the role",
        ),
        negotiation_tip=(
            "Ask what exactly is checked, when, who sees the result, and how you can respond to "
            "anything that comes up before a decision is made."
        ),
        expected_in=("employment", "lease"),
    ),
)
