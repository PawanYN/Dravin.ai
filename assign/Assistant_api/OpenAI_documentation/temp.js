{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}

openai.APIStatusError: Error code: 402 - 
{
    'error': 
        {
        'message': 'This request requires more credits, or fewer max_tokens. You requested up to 16384 tokens, but can only afford 3661. To increase, visit https://openrouter.ai/settings/credits and upgrade to a paid account', 
        'code': 402, 
        'metadata': {'provider_name': None}
        }, 
    'user_id': 'user_2zM7P6YUJbL3MfDR56phOu5jvnX'
}