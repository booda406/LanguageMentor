#!/bin/bash

# 設置顏色輸出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "Starting deployment process..."

# 檢查 Docker 是否運行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

# 確保日誌目錄存在
mkdir -p logs
touch logs/app.log
chmod 777 logs/app.log

# 停止現有容器
echo "Stopping existing containers..."
docker-compose down

# 構建新鏡像
echo "Building Docker image..."
docker-compose build --no-cache

# 運行容器
echo "Starting containers..."
docker-compose up -d

# 檢查容器狀態
echo "Checking container status..."
docker-compose ps

# 顯示日誌
echo -e "${GREEN}Deployment completed!${NC}"
echo "To view logs, run: docker-compose logs -f"
