from openai import OpenAI
import os

# Get your API key from env variable
API_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI-compatible client (for OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # OpenRouter endpoint
    api_key=API_key
)

# Call the Chat Completions API with streaming enabled
stream = client.chat.completions.create(
    model="gpt-4.1",  # You can also use "mistralai/mistral-7b-instruct" etc.
    messages=[
        {
            "role": "user",
            "content": "Say 'double bubble bath' ten times fast.",
        },
    ],
    max_tokens=500,  # ✅ Within your limit
    stream=True,
)

# Process the streaming response
for event in stream:
    print(event)

"""
openai.APIStatusError: Error code: 402 - 
{'error': 
    {
    'message':'This request requires more credits, or fewer max_tokens. 
                You requested up to 32768 tokens, but can only afford 4031. 
                To increase, visit https://openrouter.ai/settings/credits and 
                upgrade to a paid account', 
    'code': 402, 
    'metadata': {'provider_name': None}}, 
    'user_id': 'user_2zM7P6YUJbL3MfDR56phOu5jvnX'
    }
"""