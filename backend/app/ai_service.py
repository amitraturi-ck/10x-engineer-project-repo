import os
from openai import OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

def run_prompt(prompt_text: str) -> str:
    """Execute a prompt using OpenAI API."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")
