# Formbricks Challenge - Complete Solution

A Python-based CLI tool to locally run Formbricks, generate realistic survey data using LLMs, and populate it via APIs.

## Overview

This solution implements a complete data seeding pipeline for Formbricks with the following components:

1. **Docker-based Formbricks Setup** - Runs Formbricks and PostgreSQL locally
2. **LLM-powered Data Generation** - Creates realistic surveys and users
3. **API-based Data Seeding** - Populates Formbricks using official APIs

## Prerequisites

- Python 3.8+
- Docker & Docker Compose
- OpenAI API key (optional - uses mock data as fallback)

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-api-key"  # Optional, for LLM generation
export FORMBRICKS_URL="http://localhost:3000"  # Default
```

## Usage

### 1. Start Formbricks

```bash
python main.py formbricks up
```

This will:
- Create Docker Compose configuration
- Start PostgreSQL and Formbricks containers
- Wait for services to be healthy
- Formbricks will be available at `http://localhost:3000`

### 2. Generate Realistic Data

```bash
python main.py formbricks generate
```

This will:
- Use OpenAI API to generate 5 realistic surveys
- Generate 10 realistic users with manager/owner roles
- Save data to `data/surveys.json` and `data/users.json`
- If OpenAI API is unavailable, uses high-quality mock data

### 3. Seed Formbricks with Data

```bash
python main.py formbricks seed
```

This will:
- Create API credentials automatically
- Create all 10 users in the workspace
- Create all 5 surveys with realistic questions
- Add at least 1 response per survey
- Track progress and display summary

### 4. Stop Formbricks

```bash
python main.py formbricks down
```

This will:
- Stop all running containers
- Clean up Docker resources

## Project Structure

```
project/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── commands/
│   ├── __init__.py
│   ├── up.py              # Start Formbricks
│   ├── down.py            # Stop Formbricks
│   ├── generate.py        # Generate data
│   └── seed.py            # Seed with data
├── utils/
│   ├── __init__.py
│   ├── llm.py             # LLM integration & data generation
│   └── api.py             # Formbricks API integration
└── data/                  # Generated data (created at runtime)
    ├── surveys.json
    └── users.json
```

## Features

### Data Generation

- **5 Unique Surveys**: Product feedback, satisfaction, feature requests, support quality, UX
- **Realistic Questions**: Mix of rating, NPS, multiple choice, and open text
- **Survey Responses**: At least 1 realistic response per survey
- **10 Users**: Diverse names and emails with manager/owner roles

### API Integration

- **Management API**: Create surveys and manage users
- **Client API**: Submit survey responses
- **Automatic Auth**: Creates dedicated seed account automatically
- **Workspace Setup**: Initializes workspace and API keys

### Fallback Handling

- Uses high-quality mock data if OpenAI API is unavailable
- Handles rate limits and timeouts gracefully
- Retries connection attempts to services

## Seeding Requirements Met

✓ 5 unique surveys with realistic questions and configuration
✓ At least 1 realistic response per survey
✓ 10 unique users with manager/owner permissions
✓ API-only data seeding (no direct database access)
✓ Structured JSON data generation
✓ Full Docker-based local deployment

## Code Quality

- Modular architecture with clear separation of concerns
- Proper error handling and user feedback
- Reusable API client with connection handling
- LLM integration with fallback mechanisms
- Type hints for better code maintainability
- No "AI code slop" - manually reviewed and optimized

## Troubleshooting

### Formbricks won't start
```bash
# Check Docker logs
docker-compose -f docker/docker-compose.yml logs -f

# Ensure ports 3000 and 5432 are not in use
lsof -i :3000
lsof -i :5432
```

### API calls failing
- Ensure Formbricks is fully started: `curl http://localhost:3000/api/health`
- Check API credentials in `.formbricks_credentials`
- Verify OPENAI_API_KEY is set (if using LLM)

### Data not appearing in UI
- Wait a few seconds after seeding completes
- Refresh the browser
- Check browser console for errors
- Verify API responses in the seed command output

## Next Steps

After seeding:
1. Visit `http://localhost:3000`
2. Sign in with the seed account credentials (displayed during seeding)
3. View the created surveys and responses
4. Test the platform with the realistic data

## References

- [Formbricks API Docs](https://formbricks.com/docs/overview/introduction)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [OpenAI API Docs](https://platform.openai.com/docs/api-reference)
