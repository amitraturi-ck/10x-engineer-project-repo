import os
from typing import Optional
from openai import OpenAI


def run_prompt(prompt_text: str, api_key: Optional[str] = None) -> str:
    """
    Execute a prompt using OpenAI API.

    Priority for API key:
    1. Explicit parameter
    2. Environment variable (OPENAI_API_KEY)
    """

    # Priority 1: explicit param
    final_api_key = api_key or os.getenv("OPENAI_API_KEY")

    if not final_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    client = OpenAI(api_key=final_api_key)

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")
