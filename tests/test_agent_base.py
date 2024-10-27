# This is a placeholder for test_agent_base.py
import pytest
import os
import json  # Import json module
from src.agents.agent_base import AgentBase
from unittest.mock import patch, mock_open
from langchain_core.messages import HumanMessage  # Import HumanMessage

# 測試 AgentBase 的初始化
def test_agent_base_initialization():
    with patch("builtins.open", mock_open(read_data="This is a test prompt.")):
        agent = AgentBase(name="TestAgent", prompt_file="test_prompt.txt")
        assert agent.name == "TestAgent"
        assert agent.prompt_file == "test_prompt.txt"
        assert agent.session_id == "TestAgent"

# 測試從文件載入提示
def test_load_prompt():
    mock_prompt_content = "This is a test prompt."
    with patch("builtins.open", mock_open(read_data=mock_prompt_content)):
        agent = AgentBase(name="TestAgent", prompt_file="test_prompt.txt")
        assert agent.prompt == mock_prompt_content

# 測試從不存在的文件載入提示
def test_load_prompt_file_not_found():
    with pytest.raises(FileNotFoundError):
        AgentBase(name="TestAgent", prompt_file="non_existent_file.txt")

# 測試從 JSON 文件載入初始消息
def test_load_intro():
    mock_intro_content = '{"message": "Welcome!"}'
    with patch("builtins.open", mock_open(read_data=mock_intro_content)):
        with patch("json.load", return_value=json.loads(mock_intro_content)):
            agent = AgentBase(name="TestAgent", prompt_file="test_prompt.txt", intro_file="intro.json")
            assert agent.intro_messages == json.loads(mock_intro_content)

# 測試從無效的 JSON 文件載入初始消息
def test_load_intro_invalid_json():
    mock_invalid_json = '{"message": "Welcome!"'
    with patch("builtins.open", mock_open(read_data=mock_invalid_json)):
        with pytest.raises(ValueError):
            AgentBase(name="TestAgent", prompt_file="test_prompt.txt", intro_file="intro.json")

# 測試聊天機器人的創建
def test_create_chatbot():
    with patch("builtins.open", mock_open(read_data="This is a test prompt.")):
        agent = AgentBase(name="TestAgent", prompt_file="test_prompt.txt")
        assert agent.chatbot is not None
        assert agent.chatbot_with_history is not None

# 測試聊天功能
def test_chat_with_history():
    with patch("builtins.open", mock_open(read_data="This is a test prompt.")):
        with patch("src.agents.agent_base.RunnableWithMessageHistory.invoke", return_value=HumanMessage(content="Hello!")):
            agent = AgentBase(name="TestAgent", prompt_file="test_prompt.txt")
            response = agent.chat_with_history("Hi there!")
            assert response == "Hello!"

# 運行測試
if __name__ == "__main__":
    pytest.main()
