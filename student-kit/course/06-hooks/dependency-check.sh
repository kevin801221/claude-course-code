#!/bin/bash
# 在相依套件清單檔案被修改後，檢查是否有已知漏洞。
# Hook: PostToolUse (matcher: Write)
#
# 從 stdin 的 JSON 讀取目標檔案路徑（Claude Code hook 協定）。
# 來源：https://code.claude.com/docs/en/hooks

# 從 stdin 讀取 JSON 輸入（Claude Code hook 協定）
INPUT=$(cat)

# 用 sed 擷取 file_path（相容所有平台）
FILE=$(echo "$INPUT" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$FILE" ]; then
  exit 0
fi

# 用 basename 做比對 — file_path 可能是絕對路徑
BASENAME=$(basename "$FILE")

# 只在寫入相依套件清單檔案時執行
case "$BASENAME" in
  package.json|package-lock.json|yarn.lock|pnpm-lock.yaml| \
  requirements.txt|Pipfile|Pipfile.lock|pyproject.toml| \
  go.mod|go.sum| \
  Cargo.toml|Cargo.lock| \
  Gemfile|Gemfile.lock| \
  composer.json|composer.lock| \
  pom.xml|build.gradle|build.gradle.kts)
    echo "📦 相依套件清單已更新：$FILE — 正在掃描漏洞…"
    ;;
  *)
    exit 0
    ;;
esac

ISSUES_FOUND=0

# ── npm / yarn / pnpm ────────────────────────────────────────────────────────
if [[ "$BASENAME" == package*.json || "$BASENAME" == yarn.lock || "$BASENAME" == pnpm-lock.yaml ]]; then
  if command -v npm &>/dev/null; then
    echo "🔍 正在執行 npm audit…"
    if ! npm audit --audit-level=high --json 2>/dev/null | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
vulns = data.get('metadata', {}).get('vulnerabilities', {})
high = vulns.get('high', 0) + vulns.get('critical', 0)
if high:
    print(f'  ⚠️  {high} high/critical npm vulnerabilities found. Run: npm audit fix')
    sys.exit(1)
" 2>/dev/null; then
      ISSUES_FOUND=1
    else
      echo "  ✅ 沒有高風險/嚴重的 npm 漏洞"
    fi
  fi

  if command -v yarn &>/dev/null && [[ "$BASENAME" == yarn.lock ]]; then
    echo "🔍 正在執行 yarn audit…"
    if ! yarn audit --level high --json 2>/dev/null | \
        grep -q '"type":"auditAdvisory"' 2>/dev/null; then
      echo "  ✅ 沒有高風險的 yarn 漏洞"
    else
      echo "  ⚠️  yarn audit 發現漏洞。執行：yarn audit --level high"
      ISSUES_FOUND=1
    fi
  fi
fi

# ── Python ───────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == requirements.txt || "$BASENAME" == Pipfile* || "$BASENAME" == pyproject.toml ]]; then
  if command -v pip-audit &>/dev/null; then
    echo "🔍 正在執行 pip-audit…"
    if pip-audit --format=json 2>/dev/null | \
        python3 -c "
import sys, json
data = json.load(sys.stdin)
vulns = [d for d in data.get('dependencies', []) if d.get('vulns')]
if vulns:
    for dep in vulns:
        for v in dep['vulns']:
            print(f'  ⚠️  {dep[\"name\"]} {dep[\"version\"]}: {v[\"id\"]} — {v[\"fix_versions\"]}')
    sys.exit(1)
" 2>/dev/null; then
      echo "  ✅ 沒有發現 Python 漏洞"
    else
      ISSUES_FOUND=1
      echo "  執行：pip-audit 以查看詳情"
    fi
  elif command -v safety &>/dev/null; then
    echo "🔍 正在執行 safety check…"
    OUTPUT=$(safety check --short-report 2>&1)
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
      echo "  ✅ 沒有發現 Python 漏洞"
    elif echo "$OUTPUT" | grep -qiE "vulnerability|CVE|insecure"; then
      echo "$OUTPUT"
      ISSUES_FOUND=1
    else
      echo "  ⚠️  safety check 無法完成（網路或設定錯誤）" >&2
    fi
  fi
fi

# ── Go ───────────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == go.mod || "$BASENAME" == go.sum ]]; then
  if command -v govulncheck &>/dev/null; then
    echo "🔍 正在執行 govulncheck…"
    OUTPUT=$(govulncheck ./... 2>&1)
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
      echo "  ✅ 沒有發現 Go 漏洞"
    elif echo "$OUTPUT" | grep -q "Vulnerability #"; then
      echo "$OUTPUT"
      ISSUES_FOUND=1
    else
      echo "  ⚠️  govulncheck 無法完成：$OUTPUT" >&2
    fi
  fi
fi

# ── Rust ─────────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == Cargo.toml || "$BASENAME" == Cargo.lock ]]; then
  if command -v cargo-audit &>/dev/null; then
    echo "🔍 正在執行 cargo audit…"
    if ! cargo audit 2>/dev/null; then
      ISSUES_FOUND=1
    else
      echo "  ✅ 沒有發現 Rust 漏洞"
    fi
  fi
fi

# ── Ruby ─────────────────────────────────────────────────────────────────────
if [[ "$BASENAME" == Gemfile || "$BASENAME" == Gemfile.lock ]]; then
  if command -v bundler-audit &>/dev/null; then
    echo "🔍 正在執行 bundler-audit…"
    bundler-audit check --update 2>/dev/null || ISSUES_FOUND=1
  fi
fi

# ── 通用備援：trivy ──────────────────────────────────────────────────
if command -v trivy &>/dev/null; then
  echo "🔍 正在執行 trivy 檔案系統掃描…"
  if ! trivy fs --exit-code 1 --severity HIGH,CRITICAL --quiet . 2>/dev/null; then
    ISSUES_FOUND=1
  else
    echo "  ✅ trivy 沒有發現 HIGH/CRITICAL 等級問題"
  fi
fi

if [ "$ISSUES_FOUND" -eq 0 ]; then
  echo "✅ 相依套件檢查通過 — 未發現漏洞"
else
  echo ""
  echo "⚠️  發現漏洞。提交前請檢查並更新相依套件。"
  echo "   此 hook 僅供參考，不會阻擋你的工作流程。"
fi

# 一律 exit 0 — 此 hook 只警告，不阻擋
exit 0
