import json
import requests
import os

def export_free_openrouter_models(output_dir="models/free_models"):
    url = "https://openrouter.ai/api/v1/models"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Fetch data from OpenRouter API
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes
        data = response.json()

        free_models = []
        free_models_info = []

        # Step 2 & 3: Iterate and filter for free tiers
        for model in data.get("data", []):
            pricing = model.get("pricing", {})

            # Free models have string "0" for both input (prompt) and output (completion)
            if pricing.get("prompt") == "0" and pricing.get("completion") == "0":
                free_models_info.append(
                    model
                )
                free_models.append(
                    {
                        "id": model.get("id"),
                        "name": model.get("name"),
                        "context_length": model.get("context_length"),
                        # "benchmarks": model.get("benchmarks", {}),
                    }
                )

        # Step 4: Export to JSON file
        with open(f"{output_dir}/free_models_info.json", "w", encoding="utf-8") as f:
            json.dump(free_models_info, f, indent=4, ensure_ascii=False)
        with open(f"{output_dir}/free_models.json", "w", encoding="utf-8") as f:
            json.dump(free_models, f, indent=4, ensure_ascii=False)
        print(
            f"Success! Extracted {len(free_models)} free models to '{output_dir}/free_models.json'."
        )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")


if __name__ == "__main__":
    export_free_openrouter_models()