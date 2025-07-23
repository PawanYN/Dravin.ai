import os
import time
from tqdm.auto import tqdm
from pandas import DataFrame
from datasets import load_dataset
import random
import string


# Import OpenAI client and initialize with your API key.
from openai import OpenAI
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"))

# Import Pinecone client and related specifications.
from pinecone import Pinecone
from pinecone import ServerlessSpec

# Load the dataset (ensure you're logged in with huggingface-cli if needed)
ds = load_dataset("FreedomIntelligence/medical-o1-reasoning-SFT", "en", split='train[:100]', trust_remote_code=True)
ds_dataframe = DataFrame(ds)

# Merge the Question and Response columns into a single string.
ds_dataframe['merged'] = ds_dataframe.apply(
    lambda row: f"Question: {row['Question']} Answer: {row['Response']}", axis=1
)
print("Example merged text:", ds_dataframe['merged'].iloc[0])