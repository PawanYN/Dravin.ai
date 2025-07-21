from openai import OpenAI
import os

API_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", #endpoint
    api_key=API_key          #API key
)


#----------------------For image input-------------------------

# Call gpt-4o-mini vision model
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ]
)

# Print response
print(response.choices[0].message.content)
