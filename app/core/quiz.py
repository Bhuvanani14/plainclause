"""Interactive Legal Awareness Quiz Module for PlainClause.

Provides quiz questions, options, explanations, and scoring logic to test user awareness on legal document analysis and contract red flags.
"""

from __future__ import annotations

from typing import Dict, List, Any

QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "category": "Tenancy & Housing",
        "question": "A lease clause says the landlord can increase the rent 'at any time upon 7 days notice without limit'. What is the risk level of this clause?",
        "options": [
            "Low Risk: Landlords always have unlimited right to raise rent",
            "Moderate Risk: 7 days is reasonable notice",
            "Severe Risk: Uncapped rent increases with minimal notice remove financial predictability",
            "No Risk: Rent increases are illegal everywhere"
        ],
        "correct_index": 2,
        "explanation": "Severe Risk! Uncapped rent increases with minimal notice leave tenants vulnerable to arbitrary price hikes. Standard leases lock rent for the fixed term or limit increases to a statutory/inflation cap."
    },
    {
        "id": 2,
        "category": "Employment & Career",
        "question": "What is the main concern with a worldwide 2-year Non-Compete clause in an employment offer?",
        "options": [
            "It requires you to pay extra taxes",
            "It severely restricts your ability to work in your industry globally after leaving",
            "It guarantees you a promotion after 2 years",
            "It only applies if you get fired for gross misconduct"
        ],
        "correct_index": 1,
        "explanation": "A worldwide 2-year non-compete is extremely broad and can prevent you from taking new jobs in your field anywhere in the world. Reasonable non-competes are limited in time, geography, and specific role."
    },
    {
        "id": 3,
        "category": "Freelancing & Contracts",
        "question": "If a Client Master Services Agreement includes 'Net 120 Payment Terms', when will your invoice be paid?",
        "options": [
            "Within 120 hours of submitting",
            "Within 12 days of approval",
            "120 days after receipt of the invoice (4 months)",
            "On the 12th day of the next month"
        ],
        "correct_index": 2,
        "explanation": "Net 120 means payment is due 120 days (4 full months) after the invoice is received! For freelancers and small businesses, such long payment terms create severe cash flow bottlenecks. Standard terms are Net 14 or Net 30."
    },
    {
        "id": 4,
        "category": "Consumer & Apps",
        "question": "What does a 'Class Action Waiver' in a Terms of Service agreement prevent users from doing?",
        "options": [
            "Preventing you from using the app on mobile devices",
            "Joining together with other affected users to file a joint lawsuit against the company",
            "Canceling your account",
            "Filing a complaint with customer support"
        ],
        "correct_index": 1,
        "explanation": "A Class Action Waiver forces users to bring claims individually rather than pooling resources with millions of other affected users in a class action lawsuit."
    },
    {
        "id": 5,
        "category": "Intellectual Property",
        "question": "An employment agreement states that the company owns all IP created 'during free time and personal hours'. Is this standard?",
        "options": [
            "Yes, employers always own everything employees create 24/7",
            "No, standard IP clauses only assign work created during working hours or using company resources/relating to company business",
            "Yes, as long as you use your own laptop",
            "No, employees cannot own IP anyway"
        ],
        "correct_index": 1,
        "explanation": "Overbroad IP assignment clauses claiming personal side projects created off the clock are a major red flag! Ensure your contract explicitly carves out personal projects developed outside work hours without company resources."
    },
    {
        "id": 6,
        "category": "Disputes & Liability",
        "question": "What is an 'Unilateral Indemnification' clause in a contract?",
        "options": [
            "A clause where both parties share losses equally",
            "A clause that forces only ONE party (usually you) to pay for all legal costs and damages incurred by the other party",
            "A clause that forbids taking legal action",
            "An insurance policy paid for by the state"
        ],
        "correct_index": 1,
        "explanation": "Unilateral indemnities force only you to cover the other party's legal bills and damages. You should always push for mutual indemnification or cap your liability to a reasonable limit."
    }
]


def get_quiz_questions() -> List[Dict[str, Any]]:
    """Return quiz questions without revealing correct index for test execution."""
    questions = []
    for q in QUIZ_QUESTIONS:
        questions.append({
            "id": q["id"],
            "category": q["category"],
            "question": q["question"],
            "options": q["options"],
        })
    return questions


def evaluate_quiz(user_answers: Dict[int, int]) -> Dict[str, Any]:
    """Evaluate user answers and return detailed score breakdown with explanations."""
    score = 0
    total = len(QUIZ_QUESTIONS)
    results = []

    for q in QUIZ_QUESTIONS:
        qid = q["id"]
        selected = user_answers.get(str(qid))
        if selected is None:
            selected = user_answers.get(qid)

        is_correct = (selected == q["correct_index"])
        if is_correct:
            score += 1

        results.append({
            "id": qid,
            "category": q["category"],
            "question": q["question"],
            "selected_index": selected,
            "correct_index": q["correct_index"],
            "is_correct": is_correct,
            "explanation": q["explanation"],
        })

    percentage = round((score / total) * 100, 1)
    if percentage >= 80:
        level = "Legal Awareness Expert 🏆"
        badge = "Expert"
    elif percentage >= 50:
        level = "Contract Savvy Reader 🛡️"
        badge = "Intermediate"
    else:
        level = "Legal Awareness Learner 📘"
        badge = "Beginner"

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "level": level,
        "badge": badge,
        "results": results,
    }
