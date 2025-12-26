#!/usr/bin/env python3

import requests
import os
import time
from typing import Dict, Any, Optional
import uuid


class FormbricksAPI:
    """Handle interactions with Formbricks APIs"""

    def __init__(self):
        self.base_url = os.getenv("FORMBRICKS_URL", "http://localhost:3000").rstrip("/")
        self.api_key = None
        self.session_token = None
        self.workspace_id = None

        self._initialize()

    def _initialize(self):
        """Initialize API connection and get authentication"""
        print(f"Initializing Formbricks API at {self.base_url}...")

        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/api/health", timeout=5)
                if response.status_code < 500:
                    print("✓ Connected to Formbricks")
                    break
            except requests.exceptions.RequestException:
                if i < max_retries - 1:
                    print(f"  Waiting for Formbricks... ({i + 1}/{max_retries})")
                    time.sleep(2)
                else:
                    raise RuntimeError("Failed to connect to Formbricks after retries")

        self._get_or_create_credentials()

    def _get_or_create_credentials(self):
        """Get or create API credentials for seeding"""
        creds_file = ".formbricks_credentials"

        if os.path.exists(creds_file):
            with open(creds_file) as f:
                lines = f.read().strip().split("\n")
                if len(lines) >= 2:
                    self.api_key = lines[0]
                    self.workspace_id = lines[1]
                    print(f"✓ Using existing credentials")
                    return

        print("Creating Formbricks seed account...")
        email = f"seed-{uuid.uuid4().hex[:8]}@formbricks.local"
        password = f"Seed@{uuid.uuid4().hex[:16]}"

        auth_data = {
            "email": email,
            "password": password,
            "inviteToken": "",
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/auth/signup",
                json=auth_data,
                timeout=10,
            )

            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                self.session_token = result.get("session")
                print(f"✓ Account created: {email}")
            elif response.status_code == 409:
                print(f"✓ Account already exists, signing in...")
                login_data = {"email": email, "password": password}
                response = requests.post(
                    f"{self.base_url}/api/auth/signin",
                    json=login_data,
                    timeout=10,
                )
                if response.status_code == 200 or response.status_code == 201:
                    result = response.json()
                    self.session_token = result.get("session")
            else:
                raise Exception(f"Signup failed: {response.text}")

            self._get_workspace_and_api_key()

            with open(creds_file, "w") as f:
                f.write(f"{self.api_key}\n{self.workspace_id}")

        except Exception as e:
            print(f"✗ Failed to create credentials: {str(e)}")
            raise

    def _get_workspace_and_api_key(self):
        """Get workspace info and create API key"""
        headers = {"Authorization": f"Bearer {self.session_token}"}

        response = requests.get(
            f"{self.base_url}/api/v1/me",
            headers=headers,
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get user info: {response.text}")

        user_info = response.json()
        workspaces = user_info.get("workspaces", [])

        if not workspaces:
            raise Exception("No workspaces found")

        self.workspace_id = workspaces[0]["id"]
        print(f"✓ Workspace ID: {self.workspace_id}")

        api_key_response = requests.post(
            f"{self.base_url}/api/v1/workspaces/{self.workspace_id}/api-keys",
            headers=headers,
            json={"label": "Seed API Key"},
            timeout=10,
        )

        if api_key_response.status_code not in [200, 201]:
            raise Exception(f"Failed to create API key: {api_key_response.text}")

        api_key_data = api_key_response.json()
        self.api_key = api_key_data.get("apiKey")
        print(f"✓ API Key created")

    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a user in the workspace"""
        headers = self._get_headers()

        payload = {
            "email": user_data["email"],
            "name": user_data.get("name", user_data["email"]),
            "role": user_data.get("role", "manager").lower(),
        }

        response = requests.post(
            f"{self.base_url}/api/v1/workspaces/{self.workspace_id}/members/invite",
            headers=headers,
            json=payload,
            timeout=10,
        )

        if response.status_code not in [200, 201]:
            error_msg = response.text
            if "already a member" in error_msg.lower() or "already" in error_msg.lower():
                return user_data["email"]
            raise Exception(f"Failed to create user: {error_msg}")

        return user_data["email"]

    def create_survey(self, survey_data: Dict[str, Any]) -> str:
        """Create a survey in the workspace"""
        headers = self._get_headers()

        questions = survey_data.get("questions", [])
        questionnaire = []

        for q in questions:
            question_obj = {
                "id": q.get("id", str(uuid.uuid4())),
                "type": q.get("type", "openText"),
                "headline": {"default": q.get("question", "Question")},
                "required": True,
            }

            if q.get("type") == "multipleChoice":
                question_obj["choices"] = [
                    {"label": {"default": choice}} for choice in q.get("choices", [])
                ]

            if q.get("scale"):
                question_obj["scale"] = q.get("scale")

            questionnaire.append(question_obj)

        payload = {
            "name": survey_data.get("name", "Survey"),
            "description": survey_data.get("description", ""),
            "type": survey_data.get("type", "form"),
            "questions": questionnaire,
            "status": "active",
        }

        response = requests.post(
            f"{self.base_url}/api/v1/workspaces/{self.workspace_id}/surveys",
            headers=headers,
            json=payload,
            timeout=10,
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create survey: {response.text}")

        survey = response.json()
        return survey.get("id")

    def create_response(self, survey_id: str, response_data: Dict[str, Any]) -> str:
        """Create a survey response"""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "surveyId": survey_id,
            "personId": str(uuid.uuid4()),
            "data": response_data.get("data", {}),
            "finished": True,
        }

        response = requests.post(
            f"{self.base_url}/api/v1/responses",
            headers=headers,
            json=payload,
            timeout=10,
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to create response: {response.text}")

        resp = response.json()
        return resp.get("id", str(uuid.uuid4()))

    def _get_headers(self) -> Dict[str, str]:
        """Get API headers with authentication"""
        return {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }
