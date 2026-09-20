"""Occupancy provisions: repairs and sharing."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import GROUP_PEOPLE, ClauseType

OCCUPANCY_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="maintenance_obligation",
        label="Repairs and maintenance",
        group=GROUP_PEOPLE,
        summary="Decides who must fix what, and who pays for it.",
        base_severity=5,
        patterns=(
            r"keep .{0,25}(in )?good (repair|condition)",
            r"tenant shall (maintain|repair|replace)",
            r"reasonable wear and tear",
            r"(maintain|repair) the (premises|property|structure)",
            r"at (the )?tenant.{0,3}s? (own )?expense",
        ),
        keywords=("repair", "maintain", "condition", "wear"),
        why_it_matters=(
            "Repair duties decide whether a broken heating system is your problem or the "
            "landlord's. Wide keep-in-good-repair wording can be read as making you liable "
            "for the building's fundamental faults."
        ),
        watch_for=(
            "No carve-out for fair wear and tear",
            "Duties covering the structure, roof or building services",
            "No obligation on the owner to service safety equipment",
        ),
        negotiation_tip=(
            "Ask for a clear split: the owner handles structure, services and safety equipment, "
            "you handle cleanliness and minor day-to-day items, and fair wear and tear is excluded."
        ),
        expected_in=("lease",),
    ),
    ClauseType(
        id="subletting",
        label="Subletting and guests",
        group=GROUP_PEOPLE,
        summary="Whether you may share the property or take in a lodger.",
        base_severity=5,
        patterns=(
            r"sub-?let",
            r"sub-?tenan",
            r"not .{0,25}(assign|part with possession)",
            r"lodger|housemate|occupier",
            r"prior written consent",
        ),
        keywords=("sublet", "lodger", "possession", "occupier"),
        why_it_matters=(
            "A flat ban on sharing can turn a normal life event into a breach, and an absolute "
            "right to refuse consent can block a reasonable request."
        ),
        watch_for=(
            "A blanket ban with no consent route at all",
            "Consent that can be refused for any reason or charged for heavily",
            "Limits on guests staying over that are unreasonably tight",
        ),
        negotiation_tip=(
            "Ask for consent not to be unreasonably withheld or delayed, a modest fixed fee at "
            "most, and a clear allowance for guests and a lodger."
        ),
        expected_in=("lease",),
    ),
    ClauseType(
        id="entry_rights",
        label="Right of entry",
        group=GROUP_PEOPLE,
        summary="When the owner may come into your home, and on what notice.",
        base_severity=6,
        patterns=(
            r"right to enter",
            r"(landlord|owner|lessor) .{0,25}enter the (premises|property)",
            r"inspect the (premises|property)",
            r"access .{0,25}upon .{0,20}notice",
            r"without prior notice .{0,25}enter",
        ),
        keywords=("enter", "inspect", "access", "premises"),
        why_it_matters=(
            "Your home is your private space. Entry without notice or limits undermines the "
            "quiet enjoyment you are paying for."
        ),
        watch_for=(
            "Entry without notice, or notice of only a few hours",
            "Access at unreasonable hours or on unreasonable frequency",
            "A right to enter that is not limited to specific purposes",
        ),
        negotiation_tip=(
            "Ask for at least twenty-four hours notice in writing, reasonable hours, a stated "
            "purpose, and emergency access limited to genuine emergencies."
        ),
        expected_in=("lease",),
    ),
)
