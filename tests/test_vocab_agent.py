import pytest
from unittest.mock import patch, MagicMock
from src.agents.vocab_agent import VocabAgent

# 使用 pytest fixture 进行参数化设置
@pytest.fixture
def mock_get_session_history():
    with patch('src.agents.vocab_agent.get_session_history') as mock:
        yield mock

@pytest.fixture
def mock_log():
    with patch('src.agents.vocab_agent.LOG') as mock:
        yield mock

def test_restart_session(mock_get_session_history, mock_log):
    # 创建一个模拟的历史记录对象
    mock_history = MagicMock()
    mock_get_session_history.return_value = mock_history

    # 实例化 VocabAgent
    agent = VocabAgent(session_id="test_session")

    # 调用 restart_session 方法
    result = agent.restart_session()

    # 验证 get_session_history 是否被调用
    mock_get_session_history.assert_called_once_with("test_session")
    # 验证历史记录的 clear 方法是否被调用
    mock_history.clear.assert_called_once()
    # 验证日志记录是否被调用
    mock_log.debug.assert_called_once_with(f"[history][test_session]:{mock_history}")
    # 验证返回值是否为清空后的历史记录
    assert result == mock_history

def test_initialization():
    # 测试初始化
    agent = VocabAgent(session_id="test_session")
    assert agent.name == "vocab_study"
    assert agent.prompt_file == "prompts/vocab_study_prompt.txt"
    assert agent.session_id == "test_session"
