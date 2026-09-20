"""Control provisions: who decides, and who can be bound."""

from __future__ import annotations

from typing import Final

from app.core.clause_defs import GROUP_CONTROL, ClauseType

CONTROL_CLAUSES: Final[tuple[ClauseType, ...]] = (
    ClauseType(
        id="unilateral_change",
        label="Unilateral change",
        group=GROUP_CONTROL,
        summary="Lets the other side change the terms without your agreement.",
        base_severity=7,
        patterns=(
            r"may (modify|change|amend|update|vary) (these terms|this agreement|the terms)",
            r"reserve[sd]? the right to (change|modify|amend|suspend|discontinue)",
            r"amend(ed)? .{0,25}at any time",
            r"at (its|our|their) sole discretion",
            r"in (its|our) absolute discretion",
        ),
        keywords=("modify", "amend", "discretion", "sole"),
        why_it_matters=(
            "If the other side can rewrite the terms unilaterally, what you agreed is only "
            "binding on you. The protection you value most can be removed after you commit."
        ),
        watch_for=(
            "Changes effective immediately with no notice",
            "Continued use counted as acceptance, with no right to refuse",
            "Changes applied to a fixed-term deal you have already paid for",
        ),
        negotiation_tip=(
            "Ask for written notice before any change takes effect, and the right to end the "
            "agreement without penalty if you do not accept the new version."
        ),
        expected_in=("terms_of_service", "services", "partnership", "general"),
    ),
    ClauseType(
        id="assignment",
        label="Assignment and transfer",
        group=GROUP_CONTROL,
        summary="Controls whether either side can hand the agreement to someone else.",
        base_severity=4,
        patterns=(
            r"assign .{0,25}(this agreement|these terms|its rights)",
            r"may (freely )?assign",
            r"not assign .{0,30}without",
            r"transfer .{0,25}(rights|obligations) (to|under)",
            r"novation",
        ),
        keywords=("assign", "assigns", "transfer", "novation"),
        why_it_matters=(
            "An open right for them to assign means you can end up dealing with a company you "
            "never chose, while you may be barred from assigning your own rights."
        ),
        watch_for=(
            "Their assignment allowed without consent, yours restricted",
            "Assignment to a competitor or to a company with no assets",
            "No right to terminate if the agreement is assigned",
        ),
        negotiation_tip=(
            "Ask for assignment to need written consent on both sides, with an exception for a "
            "genuine group reorganisation, and a right to walk away if the other side assigns."
        ),
        expected_in=("services", "partnership", "general"),
    ),
    ClauseType(
        id="subcontracting",
        label="Subcontracting",
        group=GROUP_CONTROL,
        summary="Allows work to be passed to third parties.",
        base_severity=3,
        patterns=(
            r"sub-?contract",
            r"delegate .{0,25}(obligations|duties)",
            r"engage .{0,25}(third part|sub-?processor)",
        ),
        keywords=("subcontract", "delegate", "sub-processor"),
        why_it_matters=(
            "You stay responsible for the work even when someone else does it badly, and your "
            "information may end up with companies you have never heard of."
        ),
        watch_for=(
            "Free subcontracting with no notice to you",
            "Subcontractors given wider rights than you would agree to",
            "No obligation on the other side to supervise its subcontractors",
        ),
        negotiation_tip=(
            "Ask for notice of intended subcontractors, your approval for anything material, "
            "and confirmation that the other side stays fully responsible for their work."
        ),
        expected_in=("services", "terms_of_service", "general"),
    ),
    ClauseType(
        id="exclusivity",
        label="Exclusivity",
        group=GROUP_CONTROL,
        summary="Stops one side working with or buying from anyone else.",
        base_severity=6,
        patterns=(
            r"exclusiv(e|ely) (supplier|provider|distributor|right)",
            r"sole and exclusive",
            r"shall not .{0,30}engage .{0,30}any other",
            r"non-?circumvention",
        ),
        keywords=("exclusive", "exclusivity", "sole"),
        why_it_matters=(
            "Exclusivity can be valuable, but an exclusive tie with no minimum purchase, volume "
            "commitment or termination right can freeze out better options."
        ),
        watch_for=(
            "Exclusivity with no guaranteed minimum volumes or revenue",
            "Exclusivity lasting beyond the term, or over an unlimited territory",
            "Your side exclusive, theirs not",
        ),
        negotiation_tip=(
            "Ask for minimum volumes or guaranteed income, a defined territory and term, and an "
            "exit if the minimums are not met."
        ),
        expected_in=("services", "partnership", "general"),
    ),
    ClauseType(
        id="confidentiality",
        label="Confidentiality",
        group=GROUP_CONTROL,
        summary="Stops you sharing information you learn about the other side.",
        base_severity=3,
        patterns=(
            r"confidential information",
            r"non-?disclosure",
            r"keep .{0,25}confidential",
            r"shall not disclose",
            r"obligation of confidence",
        ),
        keywords=("confidential", "disclose", "secret"),
        why_it_matters=(
            "Most confidentiality clauses are reasonable, but a very broad definition can cover "
            "things you already knew or that are public, making the promise wider than it looks."
        ),
        watch_for=(
            "A definition including information you already had or that is public",
            "No carve-out for disclosure required by law",
            "A duty that continues forever with no time limit",
        ),
        negotiation_tip=(
            "Ask for the standard carve-outs — public knowledge, prior knowledge, independent "
            "development and legally required disclosure — plus a time limit of a few years."
        ),
        expected_in=("nda", "employment", "services", "partnership", "general"),
    ),
)
