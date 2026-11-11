#!/bin/bash

echo "🏥 系統健康檢查"
echo "===================="

ENV=${1:-production}

# 檢查 API
echo -n "API: "
if curl -sf http://api.$ENV.example.com/health > /dev/null; then
  echo "✅ 健康"
else
  echo "❌ 異常"
fi

# 檢查資料庫
echo -n "資料庫："
if pg_isready -h db.$ENV.example.com > /dev/null 2>&1; then
  echo "✅ 健康"
else
  echo "❌ 異常"
fi

# 檢查 Pod
echo -n "Kubernetes Pod: "
PODS_READY=$(kubectl get pods -n $ENV --no-headers | grep "Running" | wc -l)
PODS_TOTAL=$(kubectl get pods -n $ENV --no-headers | wc -l)
echo "$PODS_READY/$PODS_TOTAL 已就緒"

echo "===================="
