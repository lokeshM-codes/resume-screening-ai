from openai import OpenAI
from dotenv import load_dotenv
import os

#load environment vaiables
load_dotenv()

# get API key
API_KEY = os.getenv("OPENROUTER_API_KEY")

# openrouter client
client = OpenAI(
    api_key = API_KEY,
    base_url = "https://openrouter.ai/api/v1"
)

# ====================== ask ai function ========================

def ask_ai(prompt):
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b:free",
        messages = [
            {"role" : "system",
             "content" : "You are an expert AI resume assistant.Give professional and concise answer."},

             {"role" : "user",
              "content" : prompt}
        ],
        temperature = 0.7,
        max_tokens = 500
    )
    return response.choices[0].message.content

reply = ask_ai("tell me 5 important data scientist skills")
print(reply)