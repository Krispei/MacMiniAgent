import ollama
import os
from dotenv import load_dotenv
from build_prompts import build_system_prompt, build_user_prompt
from retrieval.retrieve import retrieve

load_dotenv()

histories = {}
MAX_HISTORY = 10
RETRIEVE_K = 3

MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:30b-a3b")
ollama_client = ollama.AsyncClient()

async def ask_llm(channel_id: int, user_txt: str) -> str:

    k_paths, k_chunks = retrieve(user_txt, RETRIEVE_K)

    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(user_txt, k_paths, k_chunks)

    history = histories.setdefault(channel_id, [])
    history.append({"role": "user", "content": user_prompt})

    del history[:-MAX_HISTORY]

    messages = [{"role": "system", "content": system_prompt}] + history

    print("============== INCOMING PROMPT ==============")
    print(messages)
    print("=============================================")

    resp = await ollama_client.chat(model=MODEL, messages=messages)
    reply = resp.message.content or "(no reply)"
    history.append({"role": "assistant", "content": reply})
    return reply
