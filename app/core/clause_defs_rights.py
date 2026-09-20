"""Rights provisions: restrictions placed on you, and ownership of what you make."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import GROUP_CONTROL, GROUP_RIGHTS, ClauseType

RIGHTS_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="non_compete",
        label="Non-compete restriction",
        group=GROUP_RIGHTS,
        summary="Stops you working in the same field for a period.",
        base_severity=8,
        patterns=(
            r"non-?compet(e|ition)",
            r"not (to )?compete",
            r"covenant(ing)? not to compete",
            r"restraint of trade",
            r"shall not .{0,40}(engage in|carry on|be employed by).{0,40}competing",
            r"refrain from .{0,40}compet",
        ),
        keywords=("compete", "competitor", "competition", "restraint"),
        why_it_matters=(
            "A non-compete can stop you earning a living in your own profession after the "
            "relationship ends. It is one of the most serious clauses you can sign."
        ),
        watch_for=(
            "A period of a year or more",
            "A territory or industry description so wide it covers everything you do",
            "No payment during the restricted period",
            "Restrictions surviving even if they dismiss you without cause",
        ),
        negotiation_tip=(
            "Push for the shortest realistic period, a narrow definition of competing business, "
            "a limited territory, and no restriction if they terminate you without cause."
        ),
        expected_in=("employment", "partnership", "services"),
    ),
    ClauseType(
        id="non_solicitation",
        label="Non-solicitation",
        group=GROUP_RIGHTS,
        summary="Stops you approaching their staff, clients or suppliers.",
        base_severity=6,
        patterns=(
            r"non-?solicit(ation)?",
            r"shall not .{0,35}solicit",
            r"not .{0,25}(approach|entice|poach) .{0,25}(employee|client|customer)",
            r"no-?poach",
        ),
        keywords=("solicit", "poach", "entice", "approach"),
        why_it_matters=(
            "This can cut you off from your own professional network and customers, sometimes "
            "including people who came to you first."
        ),
        watch_for=(
            "Restrictions on clients you brought with you",
            "Restrictions on responding to public advertisements",
            "Long periods, such as two years or more",
        ),
        negotiation_tip=(
            "Ask for the restriction to name only people you actually dealt with, exclude "
            "general advertising, and keep to six to twelve months."
        ),
        expected_in=("employment", "partnership", "services"),
    ),
    ClauseType(
        id="ip_assignment",
        label="Intellectual property assignment",
        group=GROUP_RIGHTS,
        summary="Transfers ownership of the things you create.",
        base_severity=7,
        patterns=(
            r"assigns? (all )?(right, title and interest|its rights)",
            r"hereby assign",
            r"work (made )?for hire",
            r"vest .{0,25}in (the )?(company|client|provider)",
            r"assign .{0,30}intellectual property",
        ),
        keywords=("assign", "vest", "inventions", "deliverables"),
        why_it_matters=(
            "This decides whether you own your own work. A wide assignment can hand over "
            "everything you create, including things made in your own time with your own kit."
        ),
        watch_for=(
            "Assignment of everything you create, with no link to your duties",
            "Assignment of pre-existing or background material you brought with you",
            "No licence back to use your own work in a portfolio",
        ),
        negotiation_tip=(
            "Limit the assignment to material created for the project, keep ownership of "
            "pre-existing work, and ask for a licence to reuse and display your work."
        ),
        expected_in=("employment", "services", "partnership", "general"),
    ),
    ClauseType(
        id="ip_ownership",
        label="Intellectual property ownership",
        group=GROUP_RIGHTS,
        summary="States who owns the ideas, content and inventions involved.",
        base_severity=4,
        patterns=(
            r"intellectual property",
            r"ownership of .{0,25}(inventions|works|deliverables|content)",
            r"all right, title and interest",
            r"moral rights",
        ),
        keywords=("intellectual", "ownership", "copyright", "inventions"),
        why_it_matters=(
            "Ownership decides who can use, sell or license the work later, and a moral rights "
            "waiver can stop you being credited for it."
        ),
        watch_for=(
            "Ownership of everything you produce, with nothing excluded",
            "A moral rights waiver that goes beyond what the project needs",
            "No clear answer about jointly created material",
        ),
        negotiation_tip=(
            "Ask for a clear list of what is transferred and what stays yours, and limit any "
            "moral rights waiver to what the project genuinely requires."
        ),
        expected_in=("employment", "services", "partnership", "general"),
    ),
    ClauseType(
        id="license_grant",
        label="Licence grant",
        group=GROUP_RIGHTS,
        summary="Gives permission to use something, usually content or software.",
        base_severity=3,
        patterns=(
            r"grants? .{0,35}(licen[cs]e|right to use)",
            r"royalty-?free",
            r"non-?exclusive licen[cs]e",
            r"worldwide, perpetual",
            r"hereby grants",
        ),
        keywords=("license", "licence", "grant", "royalty"),
        why_it_matters=(
            "The scope of a licence decides what the other side may do with your content: "
            "where, for how long, for what purpose, and whether they can pass it on."
        ),
        watch_for=(
            "Worldwide, perpetual and irrevocable, with rights to sublicense",
            "Use for marketing or model training when nobody told you",
            "No limit to the purpose or the number of users",
        ),
        negotiation_tip=(
            "Ask for the licence to be limited in purpose, territory and time, and for the right "
            "to sublicense to be removed unless it is genuinely needed."
        ),
        expected_in=("terms_of_service", "services", "general"),
    ),
    ClauseType(
        id="limitation_period",
        label="Shortened limitation period",
        group=GROUP_RIGHTS,
        summary="Cuts down how long you have to raise a complaint or claim.",
        base_severity=5,
        patterns=(
            r"waive .{0,30}right to .{0,25}(bring|commence) .{0,20}(claim|action)",
            r"within .{0,25}(months|days) .{0,25}(bring|commence|notify)",
            r"time-?barred",
            r"shall be (conclusively )?deemed .{0,25}accepted",
            r"no action .{0,25}may be (commenced|brought)",
        ),
        keywords=("waive", "commence", "claim", "period"),
        why_it_matters=(
            "A shortened window can quietly extinguish a claim before you even discover the "
            "problem, and 'deemed accepted' wording starts that clock early."
        ),
        watch_for=(
            "Twelve months or less to bring a claim",
            "Time running from delivery rather than from discovery",
            "A complaint deadline much shorter than the warranty period",
        ),
        negotiation_tip=(
            "Ask for the statutory limitation period to apply unchanged, and for time to run "
            "from when you discovered the issue rather than from delivery."
        ),
        expected_in=("services", "terms_of_service", "general"),
    ),
    ClauseType(
        id="survival",
        label="Survival after termination",
        group=GROUP_CONTROL,
        summary="Selects which promises keep going after the deal ends.",
        base_severity=4,
        patterns=(
            r"shall survive (the )?(termination|expiry|expiration)",
            r"survive .{0,25}(termination|expiry)",
            r"continues? in (full )?force .{0,25}(after|following) (termination|expiry)",
        ),
        keywords=("survive", "survival", "expiry"),
        why_it_matters=(
            "Survival clauses carry the heaviest promises — indemnities, confidentiality and "
            "restrictions — past the end of the agreement, often indefinitely."
        ),
        watch_for=(
            "Indemnities and restrictive covenants surviving forever",
            "No time limit on any surviving obligation",
            "Payment duties surviving without a matching route to recover money owed to you",
        ),
        negotiation_tip=(
            "Ask for a stated survival period, such as the applicable limitation period, and for "
            "indefinite survival to be limited to confidentiality and accrued payment rights."
        ),
        expected_in=("services", "nda", "employment", "general"),
    ),
)
