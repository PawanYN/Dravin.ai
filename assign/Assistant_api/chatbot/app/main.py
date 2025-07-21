#----------------important Libraries----------------
from app.logger import logger
logger.info("main started")

from fastapi import FastAPI 
from app.openrouter_client import assistant
import uvicorn
import app.config 
# import asyncio


#---------------meassages list for storing history and massage
messages=[                                   
          {"role": "system", "content": app.config.default_model.system_content},
        ]


#---------------FastAPI app-------------------
app=FastAPI()

@app.get("/chatbot")
async def chatbot():
      return "Here, I am to help you out by answering your questions"
    
@app.post("/chatbot/chat")
async def chat(query:str):
  
    messages.append({"role":"user","content":query})
    
    logger.info("OpenRouter assistant starting")
    result = await assistant(messages)
    print(result)
    
    messages.append({"role": "assistant",  "content":result})
    
    logger.info("OpenRouter assistant ended")
    return result

logger.info("main ended")