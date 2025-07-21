from openai import OpenAI
import os
import json
import base64
from pathlib import Path


API_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", #endpoint
    api_key=API_key          #API key
)


#----------------------File input-------------------------
# First, encode and send the PDF
def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')

# Read and encode the PDF
pdf_path = "w:/Davin.ai/assign/Dravin_new_assign/projec3/data/CV-AKHIL-v2.pdf"
base64_pdf = encode_pdf_to_base64(pdf_path)
data_url = f"data:application/pdf;base64,{base64_pdf}"

# Initial request with the PDF
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "tell me persons info - name , education and his interest from file?"
            },
            {
                "type": "file",
                "file": {
                    "filename": "document.pdf",
                    "file_data": data_url
                }
            },
        ]
    }
]

completion = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=messages
)

print(completion.choices[0].message.content)

# Name: Akhil Choudhary
# Education:
# - Graduated from IIT Kharagpur in 2022 with a CGPA of 8.93
# - Intermediate/+2 from Cambridge School Rewari in 2018 with 93%
# - Matriculation from Cambridge School Rewari in 2016 with a perfect 10.0 CGPA

# Interests:
# - Software Development
# - Machine Learning
# - Algorithms and Data Structures
# - Web Development
# - Teaching and mentoring
# - Event Management and Organizing