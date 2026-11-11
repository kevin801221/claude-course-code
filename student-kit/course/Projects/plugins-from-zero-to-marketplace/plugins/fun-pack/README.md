# fun-pack plugin

> 好玩 2 件套：冰箱食譜助手 + commit 詩人

## 內含

| 元件 | 類型 | 用途 |
|---|---|---|
| `recipe-genie` | Sub-agent | 講你冰箱有啥，給你 3 個食譜 |
| `/commit-poet` | Slash command | 把 staged diff 寫成詩當 commit message |

## 為什麼包成 plugin

純好玩、跨領域——適合演講 demo 用，觀眾會記得。

## ⚠️ 這個 plugin 是 v0.1.0

- 還沒寫測試
- recipe-genie 對亞洲食材效果較好
- commit-poet 嚴肅 repo 的同事可能會白眼

## 使用

```bash
# 食譜
> recipe-genie 我有蛋培根青菜

# 詩體 commit
> /commit-poet
（看詩，喜歡就 git commit -m "$(內容)"）
```
