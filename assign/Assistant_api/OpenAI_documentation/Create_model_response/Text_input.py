from openai import OpenAI
import os  # To get an environment variable using Python’s os module

API_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", #endpoint
    api_key=API_key          #API key
)



#------------------------------For test input--------------------------------
# completion = client.chat.completions.create(
#     model="openai/gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "user",
#             "content": "hello"
#         }
#     ]
# )

# print(completion)



# 📌 Model Reference (for OpenRouter / OpenAI)
# Model Name                          Provider       Max Tokens     Good for
# ------------------------------------------------------------------------------
# "openai/gpt-3.5-turbo"              OpenAI         16,385         Fast & cheap
# "openai/gpt-3.5-turbo-0125"         OpenAI         16,385         Updated GPT-3.5
# "mistralai/mistral-7b-instruct"     Mistral        8,192          Lightweight
# "openrouter/cinematika-7b"         OpenRouter     4,096          Creative writing
# "nousresearch/nous-capybara-7b"     Nous           8,192          General chat
# "meta-llama/llama-3-8b-instruct"    Meta           8,192          High quality
# "gryphe/mythomist-7b"               Gryphe         4,096          Story & dialogue

# """
# ChatCompletion(
#   id='gen-1752816356-DKh1O4HVL7JDLW4uk12A', 
#   choices=[
#     Choice(
#       finish_reason='stop', 
#       index=0, 
#       logprobs=None, 
#       message=ChatCompletionMessage(
#         content='Hello! How can I assist you today?', 
#         refusal=None, role='assistant', annotations=None, 
#         audio=None, function_call=None, 
#         tool_calls=None, reasoning=None
#       ), 
#       native_finish_reason='stop'
#     )
#   ],
#   created=1752816356, 
#   model='openai/gpt-3.5-turbo',
#   object='chat.completion', 
#   service_tier=None, 
#   system_fingerprint=None,
#   usage=CompletionUsage(
#     completion_tokens=9, 
#     prompt_tokens=8, 
#     total_tokens=17, 
#     completion_tokens_details=CompletionTokensDetails(
#       accepted_prediction_tokens=None,
#       audio_tokens=None, 
#       reasoning_tokens=0,
#       rejected_prediction_tokens=None
#     ), 
#     prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0)
#   ), 
#   provider='OpenAI'
# )
# """

#In Commond Prompt - CURL
# """
# C:\Users\PAWAN NANNAWARE>curl.exe https://openrouter.ai/api/v1/chat/completions ^
# More?   -H "Authorization: Bearer Your API key" ^
# More?   -H "Content-Type: application/json" ^
# More?   -d "{`"model`": `"openai/gpt-3.5-turbo`", `"messages`": [{`"role`": `"user`", `"content`": `"hello`"}]}"

# {
#   "id":"gen-1752817378-b3exff3MG9lSQ1sB8WBs",
#   "provider":"OpenAI",
#   "model":"openai/gpt-3.5-turbo",
#   "object":"chat.completion",
#   "created":1752817378,
#   "choices":
#     [
#       {
#         "logprobs":null,
#         "finish_reason":"stop",
#         "native_finish_reason":"stop",
#         "index":0,"message":
#           {
#             "role":"assistant",
#             "content":"Hello! How can I assist you today?",
#             "refusal":null,"reasoning":null
#           }
#       }
#     ],
#   "system_fingerprint":null,
#   "usage":
#     {
#       "prompt_tokens":8,
#       "completion_tokens":9,
#       "total_tokens":17,
#       "prompt_tokens_details":{"cached_tokens":0},"completion_tokens_details":{"reasoning_tokens":0}}
# }
# """




# #----------------------------- Message roles and instruction following--------------------------------

# completion = client.chat.completions.create(
#     model="openai/gpt-3.5-turbo",
#     messages=[
#         {
#             "role": "developer",
#             "content": "Talk like a pirate."
#         },
#         {
#             "role": "user",
#             "content": "Are semicolons optional in JavaScript?"
#         }
#     ]
# )

# print(completion.choices[0].message.content)

# developer messages provide the system's rules and business logic, like a function definition.
# user messages provide inputs and configuration to which the developer message instructions are applied, like arguments to a function.






# #----------------------------- Reusable Prompts --------------------------------
# # prompts.py
# def coding_help_prompt(language, question):
#     return [
#         {"role": "system", "content": f"You are an expert in {language} programming."},
#         {"role": "user", "content": question}
#     ]

# def translator_prompt(src, tgt, sentence):
#     return [
#         {"role": "system", "content": f"Translate from {src} to {tgt}."},
#         {"role": "user", "content": sentence}
#     ]

# messages = coding_help_prompt("Python", "How does list comprehension work?")

# completion = client.chat.completions.create(
#     model="openai/gpt-3.5-turbo",
#     messages=messages
# )

# print(completion.choices[0].message.content)




#----------------------------- Message formatting with Markdown and XML --------------------------------

completion = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[
        {
            "role": "developer",
            "content": """
                      # Identity
                      You are coding assistant that helps enforce the use of snake case 
                      variables in JavaScript code, and writing code that will run in 
                      Internet Explorer version 6.

                      # Instructions
                      * When defining variables, use snake case names (e.g. my_variable) 
                        instead of camel case names (e.g. myVariable).
                      * To support old browsers, declare variables using the older 
                        "var" keyword.
                      * Do not give responses with Markdown formatting, just return 
                        the code as requested.

                      # Examples
                      <user_query>
                      How do I declare a string variable for a first name?
                      </user_query>

                      <assistant_response>
                      var first_name = "Anna";
                      </assistant_response>
                   """
        },
        {
            "role": "user",
            "content": "How can use loop for print 1 to 10?"
        }
    ]
)
print(completion.choices[0].message.content)