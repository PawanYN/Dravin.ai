from app.logger import logger
logger.info("openrouter started")
from openai import OpenAI
import app.config 



#Model
async def assistant(messages:list):
    logger.debug("call to assistant")
    #Credential for openAI
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=app.config.get_api_key(),
    )
    
    try:
        response = client.chat.completions.create(       
            model=app.config.default_model.model,            
            messages=messages,
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.exception("OpenRouter call failed")     
        return None 

# if __name__ == "__main__":
#     logger.info("OpenRouter assistant starting")
#     result = asyncio.run(assistant("tell me about mango"))
#     print(result)
#     logger.info("OpenRouter assistant ended")
    
logger.info("openrouter ended")
