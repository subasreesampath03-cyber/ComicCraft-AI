import os
import json
import time

from dotenv import load_dotenv

load_dotenv()


def generate_comic_story(prompt: str):
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"

    if mock_mode:
        return {
            "title": "ComicCraft Demo",
            "panels": [
                {
                    "panel": 1,
                    "scene": f"Opening scene based on: {prompt}",
                    "dialogue": "Our adventure begins!"
                },
                {
                    "panel": 2,
                    "scene": "The main character discovers something interesting.",
                    "dialogue": "What is happening?"
                },
                {
                    "panel": 3,
                    "scene": "The character decides to take action.",
                    "dialogue": "I will find the answer!"
                },
                {
                    "panel": 4,
                    "scene": "The problem starts to get solved.",
                    "dialogue": "We are getting closer."
                },
                {
                    "panel": 5,
                    "scene": "The story reaches a happy ending.",
                    "dialogue": "We did it!"
                }
            ]
        }

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "error": "GEMINI_API_KEY is not configured."
        }

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        primary_model = os.getenv(
            "GEMINI_OUTLINE_MODEL",
            "gemini-3.8-flash"
        )

        models_to_try = [
            primary_model,
            "gemini-3.7-flash",
            "gemini-3.6-flash"
        ]

        instruction = f"""
Create a 5-panel comic story from this idea:

{prompt}

Return ONLY valid JSON using this exact structure:

{{
  "title": "Comic title",
  "panels": [
    {{
      "panel": 1,
      "scene": "scene description",
      "dialogue": "character dialogue"
    }}
  ]
}}
"""

        last_error = None

        for model in models_to_try:

            for attempt in range(3):

                try:
                    response = client.models.generate_content(
                        model=model,
                        contents=instruction
                    )

                    text = response.text.strip()

                    if text.startswith("```"):
                        text = text.replace("```json", "", 1)
                        text = text.replace("```", "", 1).strip()

                    result = json.loads(text)

                    return result

                except Exception as exc:
                    last_error = exc

                    # Wait before retrying
                    time.sleep(2 ** attempt)

            # Try the next Gemini model

        return {
            "error": f"Gemini is temporarily unavailable. Last error: {last_error}"
        }

    except Exception as exc:
        return {
            "error": f"Gemini setup failed: {exc}"
        }