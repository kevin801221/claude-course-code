# Goal 實作

![Last Updated](https://img.shields.io/badge/Last_Updated-May_13%2C_2026-white?style=flat&labelColor=555)

<table width="100%">
<tr>
<td><a href="../">← 回到 Claude Code 最佳實踐</a></td>
<td align="right"><img src="../!/claude-jumping.svg" alt="Claude" width="60" /></td>
</tr>
</table>

> 英文原文：[`implementation/claude-goal-implementation.md`](https://github.com/kevin801221/claude-code-best-practice/blob/main/implementation/claude-goal-implementation.md)

---

<a href="#社群的-goal-技巧"><img src="../!/tags/implemented-hd.svg" alt="Implemented"></a>

`/goal` 讓你的代理跨回合持續工作，直到某個條件被滿足 —— Claude Code、Codex 與 Hermes Agent 都支援。社群正逐漸收斂出幾個與它搭配極佳的高槓桿 prompt 技巧。

---

## 社群的 Goal 技巧

### 1. 請代理自己提出目標

<p align="center">
  <img src="../implementation/assets/impl-goal-claude.png" alt="Alex Finn 推文 —— /goal 是 2026 年最被低估的 AI 功能" width="50%">
</p>

> 正式確認了。Claude Code 剛發布了 /goal
>
> 2026 年最被低估的單一 AI 功能
>
> 現在 Claude Code、Codex 與 Hermes agent 都有它
>
> 它讓你的代理能完成長時間執行的任務，有時長達數天
>
> 每個人都該立刻跑這個 prompt：
>
> 『根據你對我、我的目標、企圖心，以及我們已經一起做出的東西的了解，現在有哪 3 個 /goal 是我們可以跑的、能長時間執行並產出最好成果的？』
>
> 選一個，然後請它幫你寫 prompt
>
> 你會得到幾個超強的 goal prompt 選項，讓你選用的代理完成長時間執行的任務，交出令你驚艷的成果。
>
> 今晚挪出 15 分鐘做這件事。之後再來謝我。

**來源：** [Alex Finn (@AlexFinn) on X](https://x.com/AlexFinn/status/2053976411296452887)

---

### 2. 讓代理幫你草擬 /goal prompt

<p align="center">
  <img src="../implementation/assets/impl-goal-codex.png" alt="Meta Alchemist 推文 —— Codex 的 /goal 技巧" width="50%">
</p>

> 想知道 Codex 最好的 /goal 技巧嗎？
>
> 就跟你的 Codex 說：
>
> 「讀這個 session 和這個 repo，深入分析我們在這裡想達成的確切意圖與目標，然後幫我寫出對應的 /goal prompt。
>
> 務必深挖我們的歷史與文件，做到 100% 清楚」
>
> 你也可以再加上：
>
> 「如果你對某些部分不確定，或想問我幾個問題來進一步釐清某些目標，別客氣」
>
> 然後把 Codex 給你的東西複製貼上，把開頭改成 /goal
>
> 它就會完全照你在那個 session／repo 中想做的事去做，不間斷直到完成。

**來源：** [Meta Alchemist (@meta_alchemist) on X](https://x.com/meta_alchemist/status/2054214497443995694)

---

## ![How to Use](../%21/tags/how-to-use.svg)

```bash
$ claude
> /goal <condition>
> /goal clear
```

`/goal <condition>` 讓 Claude 跨回合持續工作，直到由 Haiku 評估的條件成立。它與 `/loop`（時間驅動）和 auto 模式（逐工具）互補。需要 Claude Code v2.1.139+。

完整行為請見[官方文件](https://code.claude.com/docs/en/goal)。
