#!/bin/bash
set -e

echo "⏪ 開始回滾..."

ENV=${1:-staging}
echo "📦 目標環境：$ENV"

# 取得前一次部署
PREVIOUS=$(kubectl rollout history deployment/app -n $ENV | tail -2 | head -1 | awk '{print $1}')
echo "🔄 回滾到修訂版本：$PREVIOUS"

# 執行回滾
kubectl rollout undo deployment/app -n $ENV

# 等待回滾完成
echo "⏳ 等待回滾完成..."
kubectl rollout status deployment/app -n $ENV

# 健康檢查
echo "🏥 執行健康檢查..."
sleep 5
curl -f http://api.$ENV.example.com/health

echo "✅ 回滾完成！"
