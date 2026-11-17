# 小專案 6：Discord 文字冒險 bot（D&D 風）

> 群組沒梗了 → 開個 Discord bot 當 D&D Dungeon Master → 群組友愛和諧 ❤️

> 本範例用 **Google Gemini API**（免費額度足夠玩），不需要 Anthropic API key。
> 因為這個 bot 只用到「保持多輪對話 context」的純聊天能力，沒用到 Agent SDK 的工具/檔案操作，
> 換成 Gemini 的 chat session 幾乎是一對一對應。

## 為什麼做

- ❌ 週末群組沒梗了
- ❌ 想玩文字版 D&D 但找不到 DM
- ✅ Gemini API 寫一個有人格的 DM bot，永遠在線

## 用到的 feature

- Google Gemini API（`google-genai` Python SDK 的 async chat session）
- discord.py (Discord library)
- 一個有性格的 system prompt（放在 chat 的 `system_instruction`）

## 前置要求

1. Python 3.10+
2. Discord bot token（30 秒申請）
3. Gemini API key（Google AI Studio 免費領取：https://aistudio.google.com/apikey）

## 安裝

### Step 1：建 Discord bot

1. 開 https://discord.com/developers/applications → New Application
2. 左側 Bot → Add Bot → 複製 Token
3. **Privileged Gateway Intents** → 開啟「Message Content Intent」
4. OAuth2 → URL Generator → 勾 `bot` + `Send Messages` + `Read Message History`
5. 用產生的 URL 把 bot 加進你的 Discord server

### Step 2：裝依賴

```bash
cd 06-discord-dm-bot
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Step 3：設環境變數

```bash
cp .env.example .env
# 編輯 .env 填入你的 DISCORD_TOKEN 跟 GEMINI_API_KEY

# 載入
export $(cat .env | xargs)
```

### Step 4：啟動

```bash
python discord_dm_bot.py
```

看到 `Logged in as ...` 就成功了。

## 使用

在你的 Discord server channel 打：

```
!start          → 開新冒險
（玩家自由打字行動，bot 會回應推進故事）
!end            → 結束故事
```

## 範例對話

```
玩家：!start
Bot：你在荒原醒來，月光照在身上。遠處有座傾頹的古塔，
     塔頂閃著詭異的綠光。風吹過枯草沙沙作響。
     你怎麼做？

玩家：往古塔走過去
Bot：走了約 200 步，你來到塔下。塔門半開，裡面飄出
     腐朽的氣味。塔身刻著看不懂的符文。
     你怎麼做？

玩家：撿起一塊石頭丟進去
Bot：石頭飛進塔內，發出咚的一聲後...沉默。
     幾秒後，一個低沉的聲音從塔內傳出：
     「誰在那？」
     你怎麼做？

玩家：跑！
Bot：你轉身狂奔。20 點力量檢定...擲出 14。
     你成功跑出 100 公尺，但聽到塔內有東西
     開始追上來。心跳加速，你怎麼做？
```

## 進階變化（觀眾會喊「我也要」）

### 變化 1：場景生圖

每次描述完丟 DALL-E / Stable Diffusion API 生圖，貼回 channel：

```python
import openai
async def gen_scene_image(description: str) -> str:
    img = await openai.images.create(
        model="dall-e-3",
        prompt=f"D&D scene: {description}",
        size="1024x1024",
    )
    return img.data[0].url
```

### 變化 2：多人協作

每個玩家一個角色檔（HP、INT、STR），擲骰子用 `1d20` 套件：

```python
import random
def roll(dice: str) -> int:
    n, sides = map(int, dice.split('d'))
    return sum(random.randint(1, sides) for _ in range(n))
```

### 變化 3：存檔

Gemini chat 沒有 server 端 session id，但可以把對話歷史 dump 出來存檔，下次用 `history=` 重建：

```python
# 結束時存對話歷史（list[Content]）
history = chat.get_history()
db.save(channel_id, [c.model_dump() for c in history])

# 下次 !resume 接續
from google.genai import types
saved = [types.Content(**c) for c in db.load(channel_id)]
chat = gemini.aio.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(system_instruction=DM_PROMPT),
    history=saved,
)
```

### 變化 4：替換主題

把 `DM_PROMPT` 改成：
- 「你是科幻推理偵探，玩家在太空站醒來」
- 「你是恐怖故事說書人，玩家在廢棄醫院」
- 「你是相聲捧哏，玩家是逗哏」

## 部署（選用）

想 24/7 上線：

```bash
# Cloud Run
gcloud run deploy dm-bot --source . --region asia-east1

# 或 Fly.io
fly launch
fly secrets set DISCORD_TOKEN=... GEMINI_API_KEY=...
fly deploy
```

## 故障排除

| 症狀 | 解法 |
|---|---|
| `Improper token has been passed` | DISCORD_TOKEN 錯了，重新複製 |
| Bot 不回應訊息 | 確認「Message Content Intent」有開 |
| `GEMINI_API_KEY` 沒設 | `export GEMINI_API_KEY=...`（Google AI Studio 領） |
| `429 RESOURCE_EXHAUSTED` | 免費額度用完 — 等額度重置，或在 AI Studio 升級付費 |
| Bot 重啟後忘了之前故事 | 對話歷史沒存 — 看「變化 3」用 `get_history` 存檔 |
| 故事越玩越慢 | 對話歷史會一直變長 — 玩太久就 `!end` 重開一局 |
