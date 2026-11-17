#!/bin/zsh
# 背景監聽剪貼簿：複製英文 → 自動翻成繁中放回剪貼簿 → 直接 ⌘V
last=$(pbpaste)
while true; do
  sleep 1
  cur=$(pbpaste)
  [[ "$cur" == "$last" ]] && continue
  last=$cur
  # ponytail: 至少要有「兩個英文單字」才翻，避開密碼、token、單一詞；要更嚴格再加白名單
  [[ "$cur" =~ '[A-Za-z]+ +[A-Za-z]+' ]] || continue

  osascript -e 'display notification "翻譯中…" with title "clip-translate"'
  out=$(print -r -- "$cur" | claude -p --model haiku "把輸入翻譯成繁體中文（台灣用語），只輸出譯文，不要任何說明或前言") || continue
  print -rn -- "$out" | pbcopy
  last=$out   # 記住譯文，避免把自己的輸出再翻一次
  osascript -e 'display notification "翻好了，直接 ⌘V" with title "clip-translate"'
done
