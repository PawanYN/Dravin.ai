# Request Body Examples
# Step 1: Inference Request with Tools
# Step 2: Tool Execution (Client-Side)
# Step 3: Inference Request with Tool Results

from openai import OpenAI
import os
import json

# Get your API key from env variable
API_key = os.getenv("OPENAI_API_KEY")

# Create the OpenAI-compatible client (for OpenRouter)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # OpenRouter endpoint
    api_key=API_key
)


# #-------------------------------------------------Step1: Inference Request with Tools------------------------------------------
# tools=[
#     {
#         "type": "function",
#         "function": {
#             "name": "get_weather",
#             "description": "Get current temperature for a given location.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "City and country e.g. Bogotá, Colombia"
#                     }
#                 },
#                 "required": ["location"],
#                 "additionalProperties": False
#             }
#         }
#     }
# ]



# tools2 = [{
#     "type": "function",
#     "name": "get_weather",
#     "description": "Get current temperature for a given location.",
#     "parameters": {
#         "type": "object",
#         "properties": {
#             "location": {
#                 "type": "string",
#                 "description": "City and country e.g. Bogotá, Colombia"
#             }
#         },
#         "required": [
#             "location"
#         ],
#         "additionalProperties": False
#     }
# }]

# response = client.chat.completions.create(
#     model="gpt-4.1",
#     messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
#     max_tokens=3900,
#     tools=tools
# )

# print(response)

# # Error 1 Solved by max_tocken
# """
# openai.APIStatusError: Error code: 402 - 
# {'error': 
#     {'message': 'This request requires more credits, or fewer max_tokens.
#                     You requested up to 32768 tokens, but can only afford 3954. 
#                     To increase, visit https://openrouter.ai/settings/credits and
#                     upgrade to a paid account', 
#     'code': 402, 
#     'metadata': {'provider_name': None}}, 
#     'user_id': 'user_2zM7P6YUJbL3MfDR56phOu5jvnX'}
# """


# # Erorr 2 solved by properly definding tools-ex tools not tools2 which is wrong way

# """
# openai.BadRequestError: Error code: 400 - 
# {'error': 
#     {'message': 'Provider returned error', 
#     'code': 400, 
#     'metadata': {
#                 'raw': '{\n  
#                         "error": {\n    
#                                 "message": "Missing required parameter: \'tools[0].function\'.",\n    
#                                 "type": "invalid_request_error",\n    
#                                 "param": "tools[0].function",\n    
#                                 "code": "missing_required_parameter"\n  }
#                         \n}', 
#                 'provider_name': 'OpenAI'
#                 }
#     }, 
# 'user_id': 'user_2zM7P6YUJbL3MfDR56phOu5jvnX'}
# """

# #Final Result
# """
# ChatCompletion(
#     id='gen-1753082883-bVBfVSMZLAF5OTNr5Vxj',
#     choices=[
#         Choice(
#             finish_reason='tool_calls',
#             index=0,
#             logprobs=None,
#             message=ChatCompletionMessage(
#                 content='',
#                 refusal=None,
#                 role='assistant',
#                 annotations=None,
#                 audio=None,
#                 function_call=None,
#                 tool_calls=[
#                     ChatCompletionMessageToolCall(
#                         id='call_EKIHXQpOjNkEVl4r5veyl4YS',
#                         function=Function(
#                             arguments='{"location":"Paris, France"}',
#                             name='get_weather'
#                         ),
#                         type='function',
#                         index=0
#                     )
#                 ],
#                 reasoning=None
#             ),
#             native_finish_reason='tool_calls'
#         )
#     ],
    
#     created=1753082883,
#     model='openai/gpt-4.1',
#     object='chat.completion',
#     service_tier=None,
#     system_fingerprint=None,
#     usage=CompletionUsage(
#         completion_tokens=16,
#         prompt_tokens=65,
#         total_tokens=81,
#         completion_tokens_details=CompletionTokensDetails(
#             accepted_prediction_tokens=None,
#             audio_tokens=None,
#             reasoning_tokens=0,
#             rejected_prediction_tokens=None
#         ),
#         prompt_tokens_details=PromptTokensDetails(
#             audio_tokens=None,
#             cached_tokens=0
#         )
#     ),
#     provider='OpenAI'
# )

# """


# tool_calls = response.choices[0].message.tool_calls

# print("\n \n")
# print("-------------------------------------------------------------------------------------------------------------")
# for call in tool_calls:
#     print(f"Tool Call ID: {call.id}")
#     print(f"Function Name: {call.function.name}")
#     print(f"Arguments (raw JSON string): {call.function.arguments}")
# print("-------------------------------------------------------------------------------------------------------------")
# print("\n \n")


# """

# Fetching Data	Retrieve up-to-date information to incorporate into the model's response (RAG). Useful for searching knowledge bases and retrieving specific data from APIs (e.g. current weather data).
# Taking Action	Perform actions like submitting a form, calling APIs, modifying application state (UI/frontend or backend), or taking agentic workflow actions (like handing off the conversation).
# """

# #-------------------------------------------Step 2: Tool Execution (Client-Side)-------------------------------------
# import requests

# # def get_weather(latitude, longitude):
# #     response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
# #     data = response.json()
# #     return data['current']['temperature_2m']


# url = "https://api.weatherstack.com/current?access_key={d4cb4ca439319f6631ff80612344e6e2}"

# querystring = {"query":"New Delhi"}

# response = requests.get(url, params=querystring)

# print(response.json())

# #-------------------------------------------Step 3: Inference Request with Tool Results-------------------------------------






#----------------------------------------------------------------------------------------------------------------------------
#                                                     Function calling steps
#----------------------------------------------------------------------------------------------------------------------------

#------1. Call model with functions defined – along with your system and user messages.

tools = [
    {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
      },
    "strict": True
   }
]

input_messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=input_messages,
    max_tokens=3700,
    tools=tools,
)

#2. Model decides to call function(s) – model returns the name and input arguments.
print("\n\n -------------------------------Response-------------------------------------------")
print(response)
print("--------------------------------------------------------------------------------------\n")

"""ChatCompletion(
    id='gen-1753092928-1tY6RQy9Lcx0cA0Y7lQs',
    choices=[
        Choice(
            finish_reason='tool_calls',
            index=0,
            logprobs=None,
            message=ChatCompletionMessage(
                content='',
                refusal=None,
                role='assistant',
                annotations=None,
                audio=None,
                function_call=None,
                tool_calls=[
                    ChatCompletionMessageToolCall(
                        id='call_VWD2PxB6Nbmk1qoEVDjB8Say',
                        function=Function(
                            arguments='{"latitude":48.8566,"longitude":2.3522}',
                            name='get_weather'
                        ),
                        type='function',
                        index=0
                    )
                ],
                reasoning=None
            ),
            native_finish_reason='tool_calls'
        )
    ],
    created=1753092928,
    model='openai/gpt-4.1',
    object='chat.completion',
    service_tier=None,
    system_fingerprint=None,
    usage=CompletionUsage(
        completion_tokens=24,
        prompt_tokens=59,
        total_tokens=83,
        completion_tokens_details=CompletionTokensDetails(
            accepted_prediction_tokens=None,
            audio_tokens=None,
            reasoning_tokens=0,
            rejected_prediction_tokens=None
        ),
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=None,
            cached_tokens=0
        )
    ),
    provider='OpenAI'
)

"""

print("-----------------------------latitude and longitude-----------------------------------")
print(response. choices[0].message.tool_calls[0].function.arguments)
#Get the argument string
tool_call = response.choices[0].message.tool_calls[0]
data_str = tool_call.function.arguments
# Parse the string into a Python dictionary
data = json.loads(data_str)
latitude=data["latitude"]
longitude=data["longitude"]
print("--------------------------------------------------------------------------------------\n")



#-------------------------------------------Execute function code – parse the model's response and handle function calls.-------------------------------------
import requests

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

result = get_weather(latitude,longitude)


print("-------------------------------result = temperature--------------------------------------------")
print(result)
print("--------------------------------------------------------------------------------------\n")


#------------------------------------------Supply model with results – so it can incorporate them into its final response.-------------------
# print(tool_call)
"""
ChatCompletionMessageToolCall(
    id='call_jEb5qPgADtdV9xupXqPe1Lzc',
    function=Function(
        arguments='{"latitude":48.8566,"longitude":2.3522}',
        name='get_weather'
    ),
    type='function',
    index=0
)
"""
input_messages.append(
    {
      "role": "assistant",
      "content": None,
      "tool_calls":[tool_call] 
    }
)
# input_messages.append(tool_call)  # append model's function call message

input_messages.append({                               # append result message
    "role": "tool",
    "name":"get_weather",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

print("-------------------------------input_messages for final responce------------------------------------")
print(input_messages)
print("--------------------------------------------------------------------------------------\n")

response_2 = client.chat.completions.create(
    model="gpt-4.1",
    messages=input_messages,
    max_tokens=3600,
    tools=tools,
)


print("-------------------------------response 2------------------------------------")
print(response_2)

"""
ChatCompletion(
    id='gen-1753097890-5r7OrHna8ziNbhZNbAqp', 
    choices=[
        Choice(
            finish_reason='stop', 
            index=0, 
            logprobs=None, 
            message=ChatCompletionMessage(
                content='The current temperature in Paris today is about 18.8°C. If you need more details about the weather, such as conditions or a forecast, let me know!', 
                refusal=None, 
                role='assistant', 
                annotations=None, 
                audio=None, 
                function_call=None, 
                tool_calls=None, 
                reasoning=None
            ), 
            native_finish_reason='stop'
        )
    ], 
    created=1753097890, 
    model='openai/gpt-4.1', 
    object='chat.completion', 
    service_tier=None, 
    system_fingerprint=None, 
    usage=CompletionUsage(
        completion_tokens=35, 
        prompt_tokens=94, 
        total_tokens=129, 
        completion_tokens_details=CompletionTokensDetails(
            accepted_prediction_tokens=None, 
            audio_tokens=None, 
            reasoning_tokens=0, 
            rejected_prediction_tokens=None
        ), 
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=None, 
            cached_tokens=0
        )
    ), 
    provider='OpenAI'
)
"""

print("--------------------------------------------------------------------------------------\n")


print("-------------------------------Final Anwser about weather------------------------------")
print(response_2.choices[0].message.content)
print("--------------------------------------------------------------------------------------\n")