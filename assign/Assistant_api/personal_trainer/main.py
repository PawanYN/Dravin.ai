from dotenv import find_dotenv,load_dotenv
import json, os, sys
import openai 

#reading api key
load_dotenv(".env")
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    sys.exit("OPENROUTER_API_KEY not found in .env")
print(API_KEY)


#
client=openai.OpenAI(base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,)

model="openai/gpt-4o-mini"

#== Create our Assistant ==
personal_trainer_assis=client.beta.assistants.create(
    name="Personal Trainer",
    instructions="""You are a personal trainer assistant. You give personalized fitness advice, diet plans, and motivation.""",
    model=model
)
# assistant_id=personal_trainer_assis.id
print(personal_trainer_assis)

#== Thread ==

thread=client.beta.threads.create(
    messages=[
        {
            "role":"user",
            "content":"How do I get started working out to lose fat"
        }
    ]
)

print(thread)