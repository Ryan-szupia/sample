from joiapp_v2.config.secrets import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)