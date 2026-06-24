import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve configurations
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "google/gemma-2-9b-it:free")


def openrouter_pipeline(
    prompt, model=None, system_prompt="You are a helpful assistant.", temperature=0.7
):
    """
    A robust pipeline function to send a prompt to OpenRouter and receive a response.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "API Key missing. Please set OPENROUTER_API_KEY in your .env file."
        )

    url = "https://openrouter.ai/api/v1/chat/completions"
    target_model = model if model else DEFAULT_MODEL

    # OpenRouter headers require your app's URL and Name for their leaderboard rankings
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://localhost:3000",  # Optional, your app url
        "X-Title": "My Local AI Tool",  # Optional, your app name
        "Content-Type": "application/json",
    }

    # Structure the payload following the OpenAI chat completion format
    payload = {
        "model": target_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()
        # Parse out the actual message content from the response object
        return response_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return None
    except (KeyError, IndexError):
        print("Failed to parse response structure from OpenRouter.")
        return None


# --- Example Usage ---
if __name__ == "__main__":
    print("Testing OpenRouter Pipeline...\n")

    user_prompt = "Explain quantum computing in exactly one sentence."

    # Example 1: Using the default free model from .env
    print(f"--- Calling Default Model ({DEFAULT_MODEL}) ---")
    response = openrouter_pipeline(prompt=user_prompt)
    print(f"AI Response:\n{response}\n")

    time.sleep(0.5)  # Optional: Pause between calls to avoid rate limits

    # Example 2: Explicitly passing a different free model
    specific_free_model = "nvidia/nemotron-nano-12b-v2-vl:free"
    print(f"--- Calling Specific Model ({specific_free_model}) ---")
    response_specific = openrouter_pipeline(
        prompt=user_prompt,
        model=specific_free_model,
        system_prompt="You are a cynical pirate assistant.",
    )
    print(f"AI Response:\n{response_specific}\n")