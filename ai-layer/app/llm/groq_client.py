"""
groq_client.py
---------------
Central wrapper around the Groq API (llama-3.3) for the SkillSense AI Layer.
Every other module (mcq_generator, scenario_generator, gap_analyzer, scorer)
should call `call_llm()` instead of hitting the Groq SDK directly, so we have
one place to handle retries, timeouts, and JSON-mode parsing.
"""

import os
import json
import time
import logging
from typing import Optional

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("ai_layer.groq_client")
logging.basicConfig(level=logging.INFO)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY not set — set it in your .env file before calling the API.")

_client = Groq(api_key=GROQ_API_KEY)


class LLMCallError(Exception):
    """Raised when the LLM call fails after all retries."""
    pass


def call_llm(
    prompt: str,
    system_msg: str = "You are a helpful assistant.",
    model: str = DEFAULT_MODEL,
    temperature: float = 0.4,
    max_tokens: int = 1500,
    json_mode: bool = True,
    max_retries: int = 3,
    retry_delay_seconds: float = 2.0,
) -> str:
    """
    Call the Groq LLM and return the raw text response.

    Args:
        prompt: The user-facing prompt (task instructions + content).
        system_msg: System role instructions (persona, output rules).
        model: Groq model name.
        temperature: Lower = more deterministic. Keep low (0.2-0.5) for
                     structured outputs like MCQs and scoring.
        max_tokens: Max tokens in the response.
        json_mode: If True, asks Groq to constrain output to valid JSON.
        max_retries: Number of attempts before giving up.
        retry_delay_seconds: Delay between retries (simple linear backoff).

    Returns:
        The raw string content of the model's response.

    Raises:
        LLMCallError: if all retries fail.
    """
    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = _client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content

            if json_mode:
                # Validate it's actually parseable JSON before returning.
                json.loads(content)

            return content

        except (json.JSONDecodeError, Exception) as e:  # noqa: BLE001
            last_error = e
            logger.warning(
                "LLM call attempt %d/%d failed: %s", attempt, max_retries, e
            )
            if attempt < max_retries:
                time.sleep(retry_delay_seconds * attempt)

    raise LLMCallError(f"LLM call failed after {max_retries} attempts: {last_error}")


def call_llm_json(
    prompt: str,
    system_msg: str = "You are a helpful assistant. Always respond with valid JSON only.",
    **kwargs,
) -> dict:
    """
    Convenience wrapper: calls the LLM in JSON mode and returns a parsed dict.
    Use this from mcq_generator / gap_analyzer / scorer instead of call_llm
    when you always expect structured JSON back.
    """
    raw = call_llm(prompt=prompt, system_msg=system_msg, json_mode=True, **kwargs)
    return json.loads(raw)
