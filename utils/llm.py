#!/usr/bin/env python3

import json
import os
from typing import List, Dict, Any
import requests


def generate_surveys() -> List[Dict[str, Any]]:
    """Generate 5 realistic surveys using LLM"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠ OPENAI_API_KEY not set. Using mock data instead.")
        return generate_mock_surveys()

    prompt = """Generate exactly 5 unique, realistic survey objects for a customer feedback platform.
Each survey should have:
- name: string
- description: string
- type: "form" or "survey"
- questions: array of question objects, each with:
  - id: string (uuid format)
  - type: "openText", "multipleChoice", "rating", "nps"
  - question: string
  - choices: array (for multipleChoice)
  - scale: number (for rating/nps)
- responses: array with at least 1 realistic response object, each containing:
  - data: object with question IDs as keys and answers as values

Make surveys realistic: Product feedback, Customer satisfaction, NPS survey, Feature request survey, Support quality survey.
Return ONLY valid JSON array, no markdown formatting."""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
        )

        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"]
        surveys = json.loads(content)
        return surveys

    except Exception as e:
        print(f"⚠ LLM generation failed: {str(e)}. Using mock data instead.")
        return generate_mock_surveys()


def generate_users() -> List[Dict[str, Any]]:
    """Generate 10 realistic users using LLM"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠ OPENAI_API_KEY not set. Using mock data instead.")
        return generate_mock_users()

    prompt = """Generate exactly 10 unique, realistic user objects for a feedback platform.
Each user should have:
- email: string (realistic email address)
- name: string (realistic full name)
- role: "manager" or "owner"

Make them diverse and realistic names/emails.
Return ONLY valid JSON array, no markdown formatting."""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
        )

        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"]
        users = json.loads(content)
        return users

    except Exception as e:
        print(f"⚠ LLM generation failed: {str(e)}. Using mock data instead.")
        return generate_mock_users()


def generate_mock_surveys() -> List[Dict[str, Any]]:
    """Generate mock surveys as fallback"""
    import uuid

    surveys = [
        {
            "name": "Product Feedback Survey",
            "description": "Help us improve our product",
            "type": "form",
            "questions": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "nps",
                    "question": "How likely are you to recommend our product?",
                    "scale": 10,
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "multipleChoice",
                    "question": "Which features do you use most?",
                    "choices": ["Dashboard", "Reports", "Integrations", "API"],
                },
            ],
            "responses": [
                {
                    "data": {
                        "q1": 9,
                        "q2": "Dashboard",
                    }
                }
            ],
        },
        {
            "name": "Customer Satisfaction",
            "description": "Rate your experience with us",
            "type": "survey",
            "questions": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "rating",
                    "question": "How satisfied are you?",
                    "scale": 5,
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "openText",
                    "question": "What could we improve?",
                },
            ],
            "responses": [
                {
                    "data": {
                        "q1": 4,
                        "q2": "Better documentation needed",
                    }
                }
            ],
        },
        {
            "name": "Feature Request",
            "description": "Tell us what features you'd like",
            "type": "form",
            "questions": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "openText",
                    "question": "What feature would help you most?",
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "multipleChoice",
                    "question": "Priority level",
                    "choices": ["Low", "Medium", "High", "Critical"],
                },
            ],
            "responses": [
                {
                    "data": {
                        "q1": "Mobile app support",
                        "q2": "High",
                    }
                }
            ],
        },
        {
            "name": "Support Quality",
            "description": "Rate our support team",
            "type": "survey",
            "questions": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "rating",
                    "question": "How would you rate our support?",
                    "scale": 5,
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "openText",
                    "question": "Additional feedback",
                },
            ],
            "responses": [
                {
                    "data": {
                        "q1": 5,
                        "q2": "Great team, very responsive",
                    }
                }
            ],
        },
        {
            "name": "User Experience",
            "description": "Help us understand your experience",
            "type": "form",
            "questions": [
                {
                    "id": str(uuid.uuid4()),
                    "type": "multipleChoice",
                    "question": "How did you hear about us?",
                    "choices": ["Search", "Social Media", "Referral", "Ad"],
                },
                {
                    "id": str(uuid.uuid4()),
                    "type": "openText",
                    "question": "Your experience so far",
                },
            ],
            "responses": [
                {
                    "data": {
                        "q1": "Search",
                        "q2": "Smooth onboarding, easy to use",
                    }
                }
            ],
        },
    ]

    return surveys


def generate_mock_users() -> List[Dict[str, Any]]:
    """Generate mock users as fallback"""
    users = [
        {"email": "alice.johnson@company.com", "name": "Alice Johnson", "role": "owner"},
        {"email": "bob.smith@company.com", "name": "Bob Smith", "role": "manager"},
        {"email": "carol.williams@company.com", "name": "Carol Williams", "role": "owner"},
        {"email": "david.brown@company.com", "name": "David Brown", "role": "manager"},
        {"email": "emma.davis@company.com", "name": "Emma Davis", "role": "manager"},
        {"email": "frank.miller@company.com", "name": "Frank Miller", "role": "owner"},
        {"email": "grace.wilson@company.com", "name": "Grace Wilson", "role": "manager"},
        {"email": "henry.moore@company.com", "name": "Henry Moore", "role": "owner"},
        {"email": "iris.taylor@company.com", "name": "Iris Taylor", "role": "manager"},
        {"email": "jack.anderson@company.com", "name": "Jack Anderson", "role": "manager"},
    ]

    return users
