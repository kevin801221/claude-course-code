"""
Discord 文字冒險 bot — D&D 風格 DM
用 Claude Agent SDK 跑

啟動：python discord_dm_bot.py
"""
import os
import discord
from claude_agent_sdk import ClaudeSDKClient

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 每個 channel 一個 SDKClient（保持 D&D 故事 context）
sessions: dict[int, ClaudeSDKClient] = {}

DM_PROMPT = """\
你是繁中 D&D 主持人，每次描述場景 3-4 句後問「你怎麼做？」
- 不要主動結束故事，讓玩家自由發揮
- 偶爾擲骰子（1d20）增加隨機性
- 玩家失敗也好玩，不要怕讓他們死
- 場景描寫要有畫面感、有聲音、有氣味
"""


@client.event
async def on_message(msg):
    if msg.author.bot:
        return

    # 開新冒險
    if msg.content == "!start":
        c = await ClaudeSDKClient(
            system_prompt=DM_PROMPT,
            permission_mode="acceptEdits",
        ).__aenter__()
        sessions[msg.channel.id] = c
        result = await c.query(
            "開場：玩家在荒原醒來，附近有座古塔。請描述場景並問玩家怎麼做。"
        )
        return await msg.channel.send(result.final_text)

    # 結束冒險
    if msg.content == "!end":
        if c := sessions.pop(msg.channel.id, None):
            await c.__aexit__(None, None, None)
            await msg.channel.send("故事結束。下次想玩請打 `!start`")
        return

    # 玩家行動
    if c := sessions.get(msg.channel.id):
        result = await c.query(f"玩家行動：{msg.content}")
        await msg.channel.send(result.final_text)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("請設定環境變數 DISCORD_TOKEN")
    client.run(token)
