# rhdh-ai-refinement-bot

A web service that accepts a Jira issue description and uses the OpenAI API to return a story point estimate (Fibonacci scale), a person-days range, a priority recommendation, and a written justification — providing additional input during team refinement sessions.

## Requirements

- Python 3.11+
- An OpenAI API key

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

## Running locally

```bash
uvicorn app.main:app --reload
```

The UI is available at `http://localhost:8000` and the API at `http://localhost:8000/api/analyze`.

## API

### `GET /health`

Returns `{"status": "ok"}`.

### `POST /api/analyze`

**Request body:**
```json
{ "description": "<Jira issue description text>" }
```

**Response:**
```json
{
  "fibonacci": 5,
  "person_days": "2-3",
  "priority": "normal",
  "justification": "..."
}
```

Priority values: `blocker` | `critical` | `major` | `normal` | `minor`

## Running tests

```bash
pytest
```
