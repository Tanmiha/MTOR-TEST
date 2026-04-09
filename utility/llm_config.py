import os
from dotenv import load_dotenv

load_dotenv()


llm_config={
            "temperature": 0,
            "config_list": [
                {
                    "model": os.getenv("MODEL_NAME"),  # This should match your deployment name
                    "api_key": os.getenv("HF_TOKEN"),
                    "base_url": os.getenv("API_BASE_URL"),
                    "api_type": "azure",
                    "api_version": os.getenv("AZURE_API_VERSION")
                }
                ]
        }