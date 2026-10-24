import discord
import os
from dotenv import load_dotenv
import sys
from llm_backend import MODEL, ask_llm, histories

load_dotenv()

BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
ALLOWED_USER_ID = int(os.environ.get("ALLOWED_USER_ID", "0"))

DISCORD_LIMIT = 1990

intents=discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Ready as {client.user}, mode: {MODEL}, waiting for responses...")

@client.event
async def on_message(message: discord.Message):

    print("LOG: message sent")
    
    # message sender was the bot itself
    if message.author == client.user:
        print("LOG: message sent by bot")
        return

    dmed = isinstance(message.channel, discord.DMChannel)
    mentioned = client.user in message.mentions

    if not(dmed or mentioned):
        print("LOG: message not dmd or mentioned")
        return

    if message.author.id != ALLOWED_USER_ID:
        print(f"LOG: ignored message sent from user id: {message.author.id}")
        return

    text = message.content
    print(text)

    for tag in (f"<@{client.user.id}>", f"<@!{client.user.id}>"):
        text = text.replace(tag, "")
    text = text.strip()

    if not text:
        return

    if text.lower() == "!reset":
        histories.pop(message.channel.id, None)
        await message.channel.send("Conversation reset.")
        return

    try:
        async with message.channel.typing():
            reply = await ask_llm(message.channel.id, text)
    except Exception as e: #errror with Ollama
        reply = f"An error occured while talking with Ollama: {e}"

    for i in range(0, len(reply), DISCORD_LIMIT):
        await message.channel.send(reply[i:i+DISCORD_LIMIT])

if __name__ == "__main__":
    if not BOT_TOKEN or not ALLOWED_USER_ID:
        sys.exit("DISCORD_BOT_TOKEN and ALLOWED_USER_ID not set.")
    client.run(BOT_TOKEN)