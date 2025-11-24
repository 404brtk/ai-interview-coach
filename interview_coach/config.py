import os
from dataclasses import dataclass
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

if not os.getenv("GOOGLE_API_KEY"):
    print("ERROR: GOOGLE_API_KEY not found. Make sure your .env file exists!")


@dataclass
class AppConfiguration:
    model: str = "gemini-2.5-flash"
    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )


config = AppConfiguration()
