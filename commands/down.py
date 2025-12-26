#!/usr/bin/env python3

import subprocess
import os
from pathlib import Path


def run_down():
    """Stop and clean up the Formbricks instance"""
    print("Stopping Formbricks...")

    docker_dir = Path("docker")

    if not docker_dir.exists():
        print("✗ Docker directory not found. Was Formbricks started?")
        return

    original_cwd = os.getcwd()
    try:
        os.chdir(docker_dir)

        print("Stopping containers...")
        subprocess.run(
            ["docker-compose", "down"],
            check=True,
        )

        print("✓ Formbricks stopped successfully")

    except subprocess.CalledProcessError as e:
        print(f"✗ Error stopping Formbricks: {str(e)}")
        raise
    finally:
        os.chdir(original_cwd)
