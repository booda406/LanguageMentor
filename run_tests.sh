#!/bin/bash

echo "Running Python tests..."

# 檢查是否安裝了必要的包
pip install pytest pytest-cov coverage > /dev/null 2>&1

# 運行測試（移除重複的參數）
python -m pytest tests/ --cov=src --cov-report=xml --cov-report=term-missing

# 檢查測試結果
if [ $? -ne 0 ]; then
    echo "Tests failed! Check the output above for details."
    exit 1
fi

echo "All tests passed successfully!"
