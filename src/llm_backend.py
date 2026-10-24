import ollama
import os
from dotenv import load_dotenv

load_dotenv()

histories = {}
MAX_HISTORY = 20

ollama_client = ollama.AsyncClient()

SYSTEM_PROMPT = (
    "You are a helpful assistant. Keep Replies concise and in plain text."
)

MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:30b-a3b")

async def ask_llm(channel_id: int, user_txt: str) -> str:

    history = histories.setdefault(channel_id, [])
    history.append({"role": "user", "content": user_txt})

    
    del history[:-MAX_HISTORY]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    print("============== INCOMING PROMPT ==============")
    print(messages)
    print("=============================================")


    resp = await ollama_client.chat(model=MODEL, messages=messages)
    reply = resp.message.content or "(no reply)"
    history.append({"role": "assistant", "content": reply})
    return reply
