"""Tests for Legal AI Chat Agent & Interactive Awareness Quiz."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.chat import answer_query
from app.core.quiz import get_quiz_questions, evaluate_quiz

client = TestClient(app)


class TestChatEngine:
    def test_answer_non_compete_query(self):
        res = answer_query("What is a non-compete clause?")
        assert "Non-Compete Clause" in res["reply"]
        assert len(res["suggested_questions"]) > 0

    def test_answer_security_deposit_query(self):
        res = answer_query("Tell me about security deposit deductions")
        assert "Security Deposit" in res["reply"]

    def test_answer_fallback_query(self):
        res = answer_query("Random question about space exploration")
        assert "PlainClause" in res["reply"]

    def test_chat_api_endpoint(self):
        r = client.post("/api/chat", json={"message": "What is indemnification?"})
        assert r.status_code == 200
        data = r.json()
        assert "reply" in data
        assert "Indemnification" in data["reply"]


class TestQuizEngine:
    def test_get_quiz_questions(self):
        questions = get_quiz_questions()
        assert len(questions) >= 6
        for q in questions:
            assert "id" in q
            assert "question" in q
            assert len(q["options"]) == 4

    def test_evaluate_quiz_perfect_score(self):
        # 1: 2, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1
        answers = {"1": 2, "2": 1, "3": 2, "4": 1, "5": 1, "6": 1}
        res = evaluate_quiz(answers)
        assert res["score"] == 6
        assert res["percentage"] == 100.0
        assert "Expert" in res["level"]

    def test_quiz_api_endpoints(self):
        # GET /api/quiz
        r_get = client.get("/api/quiz")
        assert r_get.status_code == 200
        assert len(r_get.json()["questions"]) >= 6

        # POST /api/quiz/evaluate
        r_post = client.post(
            "/api/quiz/evaluate",
            json={"answers": {"1": 2, "2": 1, "3": 2, "4": 1, "5": 1, "6": 1}},
        )
        assert r_post.status_code == 200
        data = r_post.json()
        assert data["score"] == 6
        assert len(data["results"]) == 6
