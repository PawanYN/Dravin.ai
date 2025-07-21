from app.logger import logger
logger.info("confi started")

from dotenv import load_dotenv
import os, sys
from pydantic import BaseModel




# ── 1. API Key ──
load_dotenv()
def get_api_key():
    try:
      return os.getenv("OPENROUTER_API_KEY")
    except KeyError:
      logger.critical("OPENROUTER_API_KEY not found in .env — shutting down.")
      raise SystemExit(1)

# ── 2. Model Configuration ──
class model_confi(BaseModel):
    
    # Required by OpenRouter
    model:str
    system_content:str
    
    #Common tuning knobs
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False
      
GPT4O_MINI=model_confi(model="openai/gpt-4o-mini",system_content= "You are a fitness trainer assistant.")

default_model=GPT4O_MINI

logger.info("confi ended")