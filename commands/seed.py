#!/usr/bin/env python3

import json
from pathlib import Path
from utils.api import FormbricksAPI


def run_seed():
    """Seed Formbricks with generated data using APIs"""
    print("Seeding Formbricks with generated data...")

    data_dir = Path("data")

    if not data_dir.exists():
        print("✗ Data directory not found. Please run 'python main.py formbricks generate' first.")
        return

    surveys_file = data_dir / "surveys.json"
    users_file = data_dir / "users.json"

    if not surveys_file.exists() or not users_file.exists():
        print("✗ Generated data files not found. Please run 'python main.py formbricks generate' first.")
        return

    with open(surveys_file) as f:
        surveys = json.load(f)

    with open(users_file) as f:
        users = json.load(f)

    api = FormbricksAPI()

    print("\nSetting up users...")
    user_ids = {}
    for user in users:
        user_id = api.create_user(user)
        user_ids[user["email"]] = user_id
        print(f"  ✓ Created user: {user['email']}")

    print("\nCreating surveys...")
    for survey in surveys:
        survey_id = api.create_survey(survey)
        print(f"  ✓ Created survey: {survey['name']} (ID: {survey_id})")

        print(f"    Adding responses...")
        for response in survey.get("responses", []):
            api.create_response(survey_id, response)
        print(f"    ✓ Added {len(survey.get('responses', []))} responses")

    print("\n✓ Seeding complete!")
    print(f"  - Created {len(users)} users")
    print(f"  - Created {len(surveys)} surveys")
    print(f"  - Total responses: {sum(len(s.get('responses', [])) for s in surveys)}")
