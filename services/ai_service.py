"""
AI service interface for OpenRouter completions.
"""
from typing import Generator
from openai import OpenAI
from config.settings import (
    get_api_key,
    OPENROUTER_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS_STREAM,
    DEFAULT_MAX_TOKENS_STATIC
)

def get_client() -> OpenAI:
    """Instantiate and return OpenAI client dynamically."""
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Missing OPENROUTER_API_KEY. Please add OPENROUTER_API_KEY in Streamlit Cloud App Settings -> Secrets.")
    return OpenAI(
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL
    )


def ask_ai_stream(
    prompt: str,
    system_instruction: str = "You are an expert AI resume assistant. Give professional and concise answer."
) -> Generator[str, None, None]:
    """
    Query OpenRouter AI and stream back response chunks.
    """
    client = get_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS_STREAM,
        stream=True
    )

    for event in response:
        if not getattr(event, "choices", None):
            continue

        delta = event.choices[0].delta
        if not delta:
            continue

        content = getattr(delta, "content", None)
        if content:
            yield content


def ask_ai(
    prompt: str,
    system_instruction: str = "You are an expert AI resume assistant. Give professional and concise answer."
) -> str:
    """
    Query OpenRouter AI and return full static response. Falls back to static call on error.
    """
    try:
        return "".join(ask_ai_stream(prompt, system_instruction))
    except Exception:
        client = get_client()
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS_STATIC
        )
        return response.choices[0].message.content

