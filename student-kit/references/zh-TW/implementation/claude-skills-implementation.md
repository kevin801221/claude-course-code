# Skills 實作

![Last Updated](https://img.shields.io/badge/Last_Updated-Mar_02%2C_2026-white?style=flat&labelColor=555)

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`implementation/claude-skills-implementation.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/implementation/claude-skills-implementation.md)

---

<a href="#weather-svg-creatorskill"><img src="../!/tags/implemented-hd.svg" alt="Implemented"></a>

這個 repo 中實作了兩個 skills，作為 **Command → Agent → Skill** 架構模式的一部分，示範兩種不同的 skill 呼叫模式：**agent skills**（預載）與 **skills**（直接呼叫）。

---

## Weather SVG Creator（Skill）

**檔案**：[`.claude/skills/weather-svg-creator/SKILL.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/.claude/skills/weather-svg-creator/SKILL.md)

```yaml
---
name: weather-svg-creator
description: Creates an SVG weather card showing the current temperature for
  Dubai. Writes the SVG to orchestration-workflow/weather.svg and updates
  orchestration-workflow/output.md.
---

# Weather SVG Creator Skill

This skill creates a visual SVG weather card and writes the output files.

## Task
Create an SVG weather card displaying the temperature for Dubai, UAE,
and write it along with a summary to output files.

## Instructions
You will receive the temperature value and unit (Celsius or Fahrenheit)
from the calling context.

### 1. Create SVG Weather Card
Generate a clean SVG weather card...

### 2. Write SVG File
Write the SVG content to `orchestration-workflow/weather.svg`.

### 3. Write Output Summary
Write to `orchestration-workflow/output.md`...

...
```

這是一個 **skill** —— 由命令透過 Skill 工具直接呼叫。它從對話脈絡接收溫度資料，產生 SVG 天氣卡片與輸出摘要。

---

## Weather Fetcher（Agent Skill）

**檔案**：[`.claude/skills/weather-fetcher/SKILL.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/.claude/skills/weather-fetcher/SKILL.md)

```yaml
---
name: weather-fetcher
description: Instructions for fetching current weather temperature data
  for Dubai, UAE from Open-Meteo API
user-invocable: false
---

# Weather Fetcher Skill

This skill provides instructions for fetching current weather data.

## Task
Fetch the current temperature for Dubai, UAE in the requested unit
(Celsius or Fahrenheit).

## Instructions
1. Fetch Weather Data: Use the WebFetch tool to get current weather data
   - Celsius URL: https://api.open-meteo.com/v1/forecast?latitude=25.2048&longitude=55.2708&current=temperature_2m&temperature_unit=celsius
   - Fahrenheit URL: https://api.open-meteo.com/v1/forecast?latitude=25.2048&longitude=55.2708&current=temperature_2m&temperature_unit=fahrenheit
2. Extract Temperature: From the JSON response, extract `current.temperature_2m`
3. Return Result: Return the temperature value and unit clearly.

...
```

這是一個 **agent skill** —— 透過 `skills:` frontmatter 欄位在啟動時預載進 `weather-agent`。它不會被直接呼叫；而是作為注入代理脈絡的領域知識。注意 `user-invocable: false` 把它從 `/` 命令選單隱藏起來。

---

## 兩種 Skill 模式

| 模式 | 呼叫方式 | 範例 | 關鍵差異 |
|---------|-----------|---------|----------------|
| **Skill** | `Skill(skill: "name")` | `weather-svg-creator` | 透過 Skill 工具直接呼叫 |
| **Agent Skill** | 透過 `skills:` 欄位預載 | `weather-fetcher` | 啟動時注入代理脈絡 |

---

## ![How to Use](../%21/tags/how-to-use.svg)

**Skill** —— 透過 slash command 直接呼叫：
```bash
$ claude
> /weather-svg-creator
```

---

## ![How to Implement](../%21/tags/how-to-implement.svg)

請 Claude 幫你建立一個 —— 它會在 `.claude/skills/my-skill/SKILL.md` 產生帶 YAML frontmatter 與內文的 markdown 檔

# My Skill

Instructions for what the skill does.
```
