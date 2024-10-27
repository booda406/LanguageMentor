#!/bin/bash

# 設置顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# 檢查必要的命令
check_requirements() {
    echo -e "${BLUE}[STEP]${NC} Checking requirements..."
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Docker is not installed"
        exit 1
    fi
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}[ERROR]${NC} Docker Compose is not installed"
        exit 1
    fi
}

# 創建 Dockerfile
create_dockerfile() {
    echo -e "${BLUE}[STEP]${NC} Creating Dockerfile..."
    cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# 設置環境變量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案文件
COPY . .

# 創建並設置日誌目錄
RUN mkdir -p /app/logs && \
    touch /app/logs/app.log && \
    chmod 777 /app/logs/app.log

# 暴露端口
EXPOSE 7860

# 設置健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# 啟動命令
CMD ["python", "src/main.py"]
EOF
    echo -e "${GREEN}[SUCCESS]${NC} Dockerfile created"
}

# 創建 .dockerignore
create_dockerignore() {
    echo -e "${BLUE}[STEP]${NC} Creating .dockerignore..."
    cat > .dockerignore << 'EOF'
.git
.gitignore
__pycache__/
*.py[cod]
venv/
ENV/
.idea/
.vscode/
*.log
coverage.xml
docker-compose.override.yml
EOF
    echo -e "${GREEN}[SUCCESS]${NC} .dockerignore created"
}

# 創建 docker-compose.yml
create_docker_compose() {
    echo -e "${BLUE}[STEP]${NC} Creating docker-compose.yml..."
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  language-mentor:
    build: .
    container_name: language-mentor
    ports:
      - "7860:7860"
    volumes:
      - ./src:/app/src
      - ./content:/app/content
      - ./prompts:/app/prompts
      - ./logs:/app/logs
    environment:
      - ENVIRONMENT=development
      - PYTHONPATH=/app
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF
    echo -e "${GREEN}[SUCCESS]${NC} docker-compose.yml created"
}

# 創建部署腳本
create_deploy_script() {
    echo -e "${BLUE}[STEP]${NC} Creating deploy.sh..."
    cat > deploy.sh << 'EOF'
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
EOF
    chmod +x deploy.sh
    echo -e "${GREEN}[SUCCESS]${NC} deploy.sh created"
}

# 創建必要的目錄
create_directories() {
    echo -e "${BLUE}[STEP]${NC} Creating necessary directories..."
    mkdir -p logs
    touch logs/app.log
    chmod 777 logs/app.log
    echo -e "${GREEN}[SUCCESS]${NC} Directories created"
}

# 主函數
main() {
    echo "Starting Docker setup..."
    check_requirements
    create_directories
    create_dockerfile
    create_dockerignore
    create_docker_compose
    create_deploy_script
    echo -e "\n${GREEN}Setup completed!${NC}"
    echo -e "You can now run ${BLUE}./deploy.sh${NC} to build and start the container"
}

# 執行主函數
main
