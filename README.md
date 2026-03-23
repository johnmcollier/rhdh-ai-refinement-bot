# rhdh-ai-refinement-bot

A web service that accepts a Jira issue description and uses the OpenAI API to return a story point estimate (in person-days), a priority recommendation, and a written justification — providing additional input during team refinement sessions.

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
  "story_points": 3,
  "priority": "normal",
  "justification": "..."
}
```

`story_points` is a number representing estimated person-days (e.g. 0.5, 1, 2, 3, 5, 8, 13).

Priority values: `blocker` | `critical` | `major` | `normal` | `minor`

## Running tests

```bash
pytest
```

## Container

Build and run with Podman (or Docker):

```bash
podman build -t refinement-bot:latest .
podman run --rm -p 8000:8000 -e OPENAI_API_KEY=<your-key> refinement-bot:latest
```

## OpenShift deployment

See [`deploy/README.md`](deploy/README.md) for instructions on applying the OpenShift manifests (Deployment, Service, Route) and configuring the required Secret.
