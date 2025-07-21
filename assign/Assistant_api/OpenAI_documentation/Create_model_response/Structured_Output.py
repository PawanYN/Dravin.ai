from openai import OpenAI
from pydantic import BaseModel
import os  # To get an environment variable using Python’s os module

API_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", #endpoint
    api_key=API_key          #API key
)





#-----------------------------------------------------------------------------------------------------------------
# How to use Structured Outputs with text.format
# Step 1: Define your schema
# Step 2: Supply your schema in the API call
# Step 3: Handle edge cases
#-----------------------------------------------------------------------------------------------------------------




# #-------------------------------------------------Structured formate using Pydantic---------------------------
# class CalendarEvent(BaseModel):
#     name: str
#     date: str
#     participants: list[str]


# completion = client.beta.chat.completions.parse(
#     model="openai/gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "Extract the event information."},
#         {
#             "role": "user",
#             "content": "Alice and Bob are going to a science fair on Friday.",
#         },
#     ],
#     response_format=CalendarEvent,
# )

# print(completion.choices[0].message.content)

#----ERROR when model openai/gpt-3.5-turbo is used
# """
# openai.BadRequestError: 
# Error code: 400 - 
# {'error': {
#     'message': 'Provider returned error', 
#     'code': 400, 
#     'metadata': {'
#         raw': '{\n  
#             "error": 
#                 {\n    
#                     "message": "Invalid parameter: \'response_format\' of type \'json_schema\' is not supported with this model.
#                     Learn more about supported models at the Structured Outputs guide: https://platform.openai.com/docs/guides/structured-outputs",\n    
#                     "type": "invalid_request_error",\n    "param": null,\n    "code": null\n  }\n}', 'provider_name': 'OpenAI'}}, 'user_id': 'user_2zM7P6YUJbL3MfDR56phOu5jvnX'}
# """


#----Successful Output of model 
# """
# ParsedChatCompletion[CalendarEvent](
#     id='gen-1752831599-7FBOUhgAgFYPPECPFe4k', 
#     choices=[
#         ParsedChoice[CalendarEvent](
#             finish_reason='stop', 
#             index=0, logprobs=None,
#             message=ParsedChatCompletionMessage[CalendarEvent](
#                 content='{
#                     "name":"Science Fair",
#                     "date":"Friday",
#                     "participants":["Alice","Bob"]
#                     }',
#                 refusal=None, 
#                 role='assistant', 
#                 annotations=None, 
#                 audio=None, 
#                 function_call=None, 
#                 tool_calls=None, 
#                 parsed=CalendarEvent(
#                     name='Science Fair',
#                     date='Friday', 
#                     participants=['Alice', 'Bob']), 
#                     reasoning=None
#             ), 
#             native_finish_reason='stop'
#         )
#     ], 
#     created=1752831599, 
#     model='openai/gpt-4o-mini', 
#     object='chat.completion', 
#     service_tier=None,
#     system_fingerprint=None, 
#     usage=CompletionUsage(
#         completion_tokens=17, 
#         prompt_tokens=92, 
#         total_tokens=109, 
#         completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=0, rejected_prediction_tokens=None),
#         prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0)), provider='OpenAI')
# """





#-------------------------------------------------Structured formate using json schema---------------------------

# Schema={
#     "type": "json_schema",
#     "json_schema":{
#         "name": "weather",
#         "strict": True,
#         "schema":{
#             "type": "object",
#             "properties":{
#                 "location":{
#                     "type": "string",
#                     "description": "City or location name",
#                 },
#                 "temperature": {
#                     "type": "number",
#                     "description": "Temperature in Celsius",
#                 },
#                 "conditions": {
#                     "type": "string",
#                     "description": "Weather conditions description",
#                 },
            
#             },
#             "required": ["location", "temperature", "conditions"],
#             "additionalProperties": False,
#         }
#     }
# }

# completion = client.beta.chat.completions.parse(
#     model="openai/gpt-4o-mini",
#     messages= [
#          {"role": "user", "content": "What is the weather like in London?"},
#     ],
#     response_format=Schema,
# )

# print(completion.choices[0].message.content)



# #-------------------------------------------------Refusals with Structured Outputs---------------------------

# class Step(BaseModel):
#     explanation: str
#     output: str

# class MathReasoning(BaseModel):
#     steps: list[Step]
#     final_answer: str

# completion = client.beta.chat.completions.parse(
#     model="google/gemma-3-27b-it",
#     messages=[
#         {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
#         {"role": "user", "content": "how can I solve 8x +7 = -23"}
#     ],
#     response_format=MathReasoning,
# )

# math_reasoning = completion.choices[0].message

# # If the model refuses to respond, you will get a refusal message
# if (math_reasoning.refusal):
#     print(math_reasoning.refusal)
# else:
#     print(math_reasoning.parsed)
    

# 📝 Tips for Structured Outputs:

# 1. Handle user input: Prompt the model to return empty/default values 
#    or a clear message when input doesn't fit the task.

# 2. Guard against hallucinations: The model may force-fit bad input to the schema.

# 3. Expect errors: Mistakes can still happen. Use examples or split tasks if needed.

# 4. Avoid schema drift: Use Pydantic (Python) or Zod (JS) to keep JSON Schema synced with code.

# 5. Optional: Add CI rules to auto-sync schema and type definitions to prevent mismatch.



#-------------------------------------------------Streaming with Structured OutPut---------------------------

# from typing import List

# class EntitiesModel(BaseModel):
#     attributes: List[str]
#     colors: List[str]
#     animals: List[str]


# with client.responses.stream(
#     model="gpt-4.1",
#     input=[
#         {"role": "system", "content": "Extract entities from the input text"},
#         {
#             "role": "user",
#             "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes",
#         },
#     ],
#     text_format=EntitiesModel,
# ) 

#----------------------------------Q1-----------------------

# question = "How would you build the tallest building ever?"
# completion = client.chat.completions.create(
#     model="openai/gpt-4o-mini",
#     messages= [
#         {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step.each step in each stream it should one single like not new line"},
#         {"role": "user", "content": "how can I solve 8x +7 = -23"}
#     ],
#     stream=True
# )

# for event in completion:
#     print(event.choices[0].delta.content ,end="")


#------------------------------------Q2-----------------------

#--------------using pydantic-----
# from typing import List

# class EntitiesModel(BaseModel):
#     attributes: List[str]
#     colors: List[str]
#     animals: List[str]
   
#--------------using JSON Schema-----
# Schema = {
#     "type": "json_schema",
#     "json_schema": {
#         "name": "Entities",
#         "strict": True,
#         "schema": {
#             "type": "object",
#             "description": "Extract lists of attributes, colors, and animals.",
#             "properties": {
#                 "attribute": {
#                     "type": "array",
#                     "description": "List of attributes",
#                     "items": {
#                         "type": "string"
#                     }
#                 },
#                 "colors": {
#                     "type": "array",
#                     "description": "List of color names",
#                     "items": {
#                         "type": "string"
#                     }
#                 },
#                 "animals": {
#                     "type": "array",
#                     "description": "List of animal names",
#                     "items": {
#                         "type": "string"
#                     }
#                 }
#             },
#             "required": ["attribute", "colors", "animals"],
#             "additionalProperties": False
#         }
#     }
# }


# completion = client.chat.completions.create(
#     model="openai/gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "Extract entities(attribute , colors , animals in separate list) from the input text"},
#         {
#             "role": "user",
#             "content": "The quick brown fox jumps over the lazy dog with piercing blue eyes",
#         },
#     ],
#     response_format=Schema,
#     stream=True
# )

# import time
# for event in completion:
#     print(event.choices[0].delta.content ,end="")
#     time.sleep(0.001)

#------------------------------------Q3-----------------------

question = "How would you build the tallest building ever?"
completion = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content":question  ,
        },
    ],
    stream=True
)

import time
for event in completion:
    print(event.choices[0].delta.content ,end="")
    time.sleep(0.01)

"""
ChatCompletionChunk(
    id='gen-1752836906-XtwhcrqHy5SjvcNGt7Xi', 
    choices=[Choice(delta=ChoiceDelta(content='', function_call=None, refusal=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None, native_finish_reason=None)], created=1752836906, model='openai/gpt-4o-mini', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=673, prompt_tokens=16, total_tokens=689, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=0, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0)), provider='OpenAI')
"""

#------------------------------------Q4-----------------------
import json

question = "How would you build the tallest building ever?"

buffer = ""

with client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        stream=True
) as r:
    for chunk in r.iter_content(chunk_size=1024, decode_unicode=True):
        buffer += chunk
        while True:
            try:
                # Find the next complete SSE line
                line_end = buffer.find('\n')
                if line_end == -1:
                 break

                line = buffer[:line_end].strip()
                buffer = buffer[line_end + 1:]

                if line.startswith('data: '):
                    data = line[6:]
                    if data == '[DONE]':
                        break

                    try:
                        data_obj = json.loads(data)
                        content = data_obj["choices"][0]["delta"].get("content")
                        if content:
                            print(content, end="", flush=True)
                    except json.JSONDecodeError:
                        pass
            except Exception:
                break



"""
import httpx

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json",
}
data = {
    "model": "openai/gpt-4o-mini",
    "messages": [{"role": "user", "content": "Tell me a joke."}],
    "stream": True
}

with httpx.stream("POST", url, headers=headers, json=data, timeout=None) as response:
    for line in response.iter_lines():
        if line.strip().startswith("data: "):
            content = line.strip()[6:]
            if content == "[DONE]":
                break
            print(content)

"""


# Supported JSON Schema types for Structured Outputs
# These can be used when defining "type" in a schema:
# - string
# - number
# - boolean
# - integer
# - object
# - array
# - enum
# - anyOf

# Supported string constraints:
# - pattern: A regular expression the string must match
# - format: Predefined string formats:
#     - "date-time"
#     - "time"
#     - "date"
#     - "duration"
#     - "email"
#     - "hostname"
#     - "ipv4"
#     - "ipv6"
#     - "uuid"

# Supported number constraints:
# - multipleOf: Value must be a multiple of this number
# - maximum: Value must be ≤ this
# - exclusiveMaximum: Value must be < this
# - minimum: Value must be ≥ this
# - exclusiveMinimum: Value must be > this

# Supported array constraints:
# - minItems: Minimum number of elements required
# - maxItems: Maximum number of elements allowed

# Example usage in a schema:
example_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"  # must be a valid email address
        },
        "scores": {
            "type": "array",
            "minItems": 1,
            "maxItems": 5,
            "items": {"type": "number", "minimum": 0}
        },
        "uuid": {
            "type": "string",
            "format": "uuid"  # must be a valid UUID
        }
    },
    "required": ["email", "scores"]
}

