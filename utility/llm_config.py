import os
from dotenv import load_dotenv

load_dotenv()

# Determine the API Key using multiple possible environment variable names
# The Scaler judge might use AZURE_OPENAI_API_KEY or OPENAI_API_KEY
api_key = os.getenv("HF_TOKEN") or os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

llm_config = {
    "temperature": 0,
    "config_list": [
        {
            "model": os.getenv("MODEL_NAME", "mtor-gpt"),  # Defaulting helps prevent crashes
            "api_key": api_key,
            "base_url": os.getenv("API_BASE_URL", os.getenv("AZURE_OPENAI_ENDPOINT")),
            "api_type": "azure",
            "api_version": os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
        }
    ]
}
