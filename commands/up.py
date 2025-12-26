#!/usr/bin/env python3

import os
import subprocess
import time
import requests
from pathlib import Path


def create_docker_compose():
    """Create docker-compose.yml for Formbricks"""
    docker_compose_content = """version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: formbricks
      POSTGRES_PASSWORD: formbricks
      POSTGRES_DB: formbricks
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U formbricks"]
      interval: 10s
      timeout: 5s
      retries: 5

  formbricks:
    image: formbricks/formbricks:latest
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DATABASE_URL: "postgresql://formbricks:formbricks@postgres:5432/formbricks"
      NEXTAUTH_SECRET: "your-secret-key-change-in-production"
      NEXTAUTH_URL: "http://localhost:3000"
    ports:
      - "3000:3000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
"""

    docker_dir = Path("docker")
    docker_dir.mkdir(exist_ok=True)

    compose_file = docker_dir / "docker-compose.yml"
    compose_file.write_text(docker_compose_content)
    print(f"Created docker-compose.yml at {compose_file}")


def wait_for_service(url, max_retries=30, delay=2):
    """Wait for service to be healthy"""
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 500:
                return True
        except requests.exceptions.RequestException:
            pass

        if i < max_retries - 1:
            print(f"Waiting for Formbricks to be ready... ({i + 1}/{max_retries})")
            time.sleep(delay)

    return False


def run_up():
    """Start Formbricks locally using Docker Compose"""
    print("Starting Formbricks locally...")

    create_docker_compose()

    docker_dir = Path("docker")
    os.chdir(docker_dir)

    try:
        print("Pulling Docker images...")
        subprocess.run(
            ["docker-compose", "pull"],
            check=True,
            capture_output=True,
        )

        print("Starting services with docker-compose...")
        subprocess.run(
            ["docker-compose", "up", "-d"],
            check=True,
        )

        os.chdir("..")

        print("Waiting for Formbricks to be ready...")
        if wait_for_service("http://localhost:3000/api/health"):
            print("✓ Formbricks is running at http://localhost:3000")
            print("✓ PostgreSQL is running on localhost:5432")
        else:
            print("✗ Formbricks failed to start properly")
            print("Check docker logs: docker-compose -f docker/docker-compose.yml logs")
            raise RuntimeError("Formbricks startup timeout")

    except subprocess.CalledProcessError as e:
        os.chdir("..")
        print(f"✗ Failed to start Formbricks: {str(e)}")
        raise
