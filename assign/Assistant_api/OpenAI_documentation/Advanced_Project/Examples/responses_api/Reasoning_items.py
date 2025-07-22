from openai import OpenAI
import os
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

response = client.completions.create(
    model="o4-mini",
    prompt="tell me a joke",
    max_tokens=6000,
)

import json

print(json.dumps(response.model_dump(), indent=2))