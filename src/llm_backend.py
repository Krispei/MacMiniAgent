import ollama
import os
from dotenv import load_dotenv
from build_prompts import build_system_prompt, build_user_prompt
from retrieval.retrieve import retrieve
import asyncio

load_dotenv()

histories = {}
MAX_HISTORY = 10
RETRIEVE_K = 3
ns_to_s = 1e9

MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:30b-a3b")
ollama_client = ollama.AsyncClient()

async def ask_llm(channel_id: int, user_txt: str) -> str:

    k_paths, k_chunks = retrieve(user_txt, RETRIEVE_K)
    
    #await asyncio.to_thread(retrieve, user_txt, RETRIEVE_K)
    
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(user_txt, k_paths, k_chunks)

    history = histories.setdefault(channel_id, [])
    history.append({"role": "user", "content": user_prompt})

    del history[:-MAX_HISTORY]

    messages = [{"role": "system", "content": system_prompt}] + history

    print("============== INCOMING PROMPT ==============")
    print(messages)
    print("=============================================")

    resp = await ollama_client.chat(model=MODEL, messages=messages, think=False)

    print(f"Total: {resp.total_duration / ns_to_s:.3f} s")
    print(f"Loading: {resp.load_duration / ns_to_s:.3f} s")
    print(f"Prefill : {resp.prompt_eval_duration / ns_to_s:.3f} s")
    print(f"Decode: {resp.eval_duration / ns_to_s:.3f} s")
    print(f"ITL: {resp.eval_duration/(resp.prompt_eval_count * ns_to_s):.3f} s")
    print(f"Total output tokens: {resp.eval_count}")

    reply = resp.message.content or "(no reply)"
    history.append({"role": "assistant", "content": reply})
    return reply
