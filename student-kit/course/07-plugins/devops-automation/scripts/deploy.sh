#!/bin/bash
set -e

echo "🚀 開始部署..."

# 載入環境設定
ENV=${1:-staging}
echo "📦 目標環境：$ENV"

# 部署前檢查
echo "✓ 執行部署前檢查..."
npm run lint
npm test

# 建置
echo "🔨 建置應用程式..."
npm run build

# 部署
echo "🚢 部署到 $ENV..."
kubectl apply -f k8s/$ENV/

# 健康檢查
echo "🏥 執行健康檢查..."
sleep 10
curl -f http://api.$ENV.example.com/health

echo "✅ 部署完成！"
