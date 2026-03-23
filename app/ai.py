import json

from openai import OpenAI

from .config import settings
from .models import AnalyzeResponse

SYSTEM_PROMPT = """You are an expert software project estimator helping a development team during refinement sessions.

Given a Jira issue description, respond with a JSON object containing exactly these fields:
- "fibonacci": integer story point estimate using only values: 1, 2, 3, 5, 8, 13, 21
- "person_days": string range estimate (e.g. "0.5-1", "1-2", "2-3", "3-5", "5-8", "8-13", "13+")
- "priority": one of "blocker", "critical", "major", "normal", "minor"
- "justification": string explaining your sizing and priority decisions

Fibonacci scale guidance:
- 1:  Trivial change, well-understood, < half a day
- 2:  Small, clear task with minimal risk, ~0.5-1 day
- 3:  Small-medium task with some complexity or unknowns, ~1-2 days
- 5:  Medium task, moderate complexity, ~2-3 days
- 8:  Large task or significant uncertainty, ~3-5 days
- 13: Very large, complex, or poorly-defined; needs careful scoping, ~5-8 days
- 21: Extremely large; should be broken down before implementation, 8+ days

Priority guidance:
- blocker:  Prevents a release or blocks critical functionality entirely
- critical: Severe user-facing impact, no acceptable workaround
- major:    Significant impact on functionality or user experience
- normal:   Standard feature or improvement with moderate impact
- minor:    Nice-to-have, cosmetic, or very low user impact

Respond with valid JSON only — no markdown, no explanation outside the JSON object."""


def analyze_issue(description: str) -> AnalyzeResponse:
    client = OpenAI(api_key=settings.openai_api_key)

    response = client.chat.completions.create(
        model=settings.openai_model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Analyze this Jira issue description and provide a sizing and priority estimate:\n\n{description}",
            },
        ],
    )

    data = json.loads(response.choices[0].message.content)
    return AnalyzeResponse(**data)
