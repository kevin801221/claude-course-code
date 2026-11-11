"""
Discord 文字冒險 bot — D&D 風格 DM
用 Google Gemini API 跑

啟動：python discord_dm_bot.py
"""
import os
import discord
from google import genai
from google.genai import types
from google.genai.chats import AsyncChat

# Gemini client（讀 GEMINI_API_KEY）
gemini = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 每個 channel 一個 chat session（保持 D&D 故事 context）
sessions: dict[int, AsyncChat] = {}

DM_PROMPT = """\
你是繁中 D&D 主持人，每次描述場景 3-4 句後問「你怎麼做？」
- 不要主動結束故事，讓玩家自由發揮
- 偶爾擲骰子（1d20）增加隨機性
- 玩家失敗也好玩，不要怕讓他們死
- 場景描寫要有畫面感、有聲音、有氣味
"""


def new_chat() -> AsyncChat:
    # system_instruction 放在 config，等同原本的 system_prompt
    return gemini.aio.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(system_instruction=DM_PROMPT),
    )


@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    # 開新冒險
    if msg.content == "!start":
        chat = new_chat()
        sessions[msg.channel.id] = chat
        resp = await chat.send_message(
            "開場：玩家在荒原醒來，附近有座古塔。請描述場景並問玩家怎麼做。"
        )
        return await msg.channel.send(resp.text)

    # 結束冒險
    if msg.content == "!end":
        if sessions.pop(msg.channel.id, None):
            await msg.channel.send("故事結束。下次想玩請打 `!start`")
        return

    # 玩家行動
    if chat := sessions.get(msg.channel.id):
        resp = await chat.send_message(f"玩家行動：{msg.content}")
        await msg.channel.send(resp.text)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("請設定環境變數 DISCORD_TOKEN")
    if not os.environ.get("GEMINI_API_KEY"):
        raise RuntimeError("請設定環境變數 GEMINI_API_KEY")
    client.run(token)
