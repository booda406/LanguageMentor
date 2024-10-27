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
