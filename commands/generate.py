#!/usr/bin/env python3

import json
import os
from pathlib import Path
from utils.llm import generate_surveys, generate_users


def run_generate():
    """Generate realistic survey and user data using LLM"""
    print("Generating realistic survey and user data...")

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    print("\nGenerating 5 unique surveys...")
    surveys = generate_surveys()

    surveys_file = data_dir / "surveys.json"
    with open(surveys_file, "w") as f:
        json.dump(surveys, f, indent=2)
    print(f"✓ Saved surveys to {surveys_file}")

    print("\nGenerating 10 unique users...")
    users = generate_users()

    users_file = data_dir / "users.json"
    with open(users_file, "w") as f:
        json.dump(users, f, indent=2)
    print(f"✓ Saved users to {users_file}")

    print("\n✓ Data generation complete!")
    print(f"  - Surveys: {surveys_file}")
    print(f"  - Users: {users_file}")
