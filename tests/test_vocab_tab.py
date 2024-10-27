import pytest
from unittest.mock import patch, MagicMock, mock_open
import gradio as gr
from src.tabs.vocab_tab import (
    create_vocab_tab,
    get_page_desc,
    restart_vocab_study_chatbot,
    handle_vocab,
    vocab_agent,
    feature
)
from src.agents.vocab_agent import VocabAgent

# Test vocabulary page description loading
def test_get_page_desc():
    # Test successful file reading
    mock_content = "This is a test vocabulary study description"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = get_page_desc(feature)
        assert result == mock_content

    # Test file not found error
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("src.tabs.vocab_tab.LOG") as mock_log:
            result = get_page_desc(feature)
            assert result == "词汇学习介绍文件未找到。"
            mock_log.error.assert_called_once_with(
                f"词汇学习介绍文件 content/page/{feature}.md 未找到！"
            )

# Test vocabulary chatbot restart
def test_restart_vocab_study_chatbot():
    # Mock VocabAgent
    mock_agent = MagicMock()
    mock_agent.chat_with_history.return_value = "Let's start learning new words!"

    with patch('src.tabs.vocab_tab.vocab_agent', mock_agent):
        chatbot = restart_vocab_study_chatbot()

        # Verify the chatbot initialization
        assert isinstance(chatbot, gr.Chatbot)
        mock_agent.restart_session.assert_called_once()
        mock_agent.chat_with_history.assert_called_once_with("Let's do it")

        expected_value = [["Let's do it", "Let's start learning new words!"]]
        assert chatbot.value == expected_value
        assert chatbot.height == 800


# Test vocabulary message handling
def test_handle_vocab():
    # Mock VocabAgent and logger
    mock_agent = MagicMock()
    mock_agent.chat_with_history.return_value = "Here's your next word!"

    with patch('src.tabs.vocab_tab.vocab_agent', mock_agent), \
         patch('src.tabs.vocab_tab.LOG') as mock_log:

        # Test normal conversation
        chat_history = []
        result = handle_vocab("Next word please", chat_history)

        assert result == "Here's your next word!"
        mock_agent.chat_with_history.assert_called_once_with("Next word please")
        mock_log.info.assert_called_once_with("[Vocab ChatBot]: Here's your next word!")

# Test vocabulary tab creation
def test_create_vocab_tab():
    with patch('gradio.Tab') as mock_tab, \
         patch('gradio.Markdown') as mock_markdown, \
         patch('gradio.Chatbot') as mock_chatbot, \
         patch('gradio.ClearButton') as mock_clear_button, \
         patch('gradio.ChatInterface') as mock_chat_interface, \
         patch('src.tabs.vocab_tab.get_page_desc') as mock_get_desc:

        # Setup mock returns
        mock_chatbot.return_value = MagicMock()
        mock_clear_button.return_value = MagicMock()
        mock_chat_interface.return_value = MagicMock()
        mock_get_desc.return_value = "Test description"

        # Create a context manager for Tab
        mock_tab_ctx = MagicMock()
        mock_tab.return_value.__enter__.return_value = mock_tab_ctx

        # Call the function
        create_vocab_tab()

        # Verify Tab creation
        mock_tab.assert_called_once_with("单词")

        # Verify components creation
        mock_markdown.assert_any_call("## 闯关背单词")
        mock_get_desc.assert_called_once_with(feature)

        # Verify Chatbot creation
        mock_chatbot.assert_called_once_with(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>开始学习新单词吧！",
            height=800
        )

        # Verify Clear Button creation
        mock_clear_button.assert_called_once_with(value="下一关")

        # Verify ChatInterface creation
        mock_chat_interface.assert_called_once()
        chat_interface_args = mock_chat_interface.call_args[1]
        assert chat_interface_args['fn'] == handle_vocab
        assert chat_interface_args['retry_btn'] is None
        assert chat_interface_args['undo_btn'] is None
        assert chat_interface_args['clear_btn'] is None
        assert chat_interface_args['submit_btn'] == "发送"

# Test vocab agent initialization
def test_vocab_agent_initialization():
    assert isinstance(vocab_agent, VocabAgent)

# Test error handling in vocab handling
def test_handle_vocab_error():
    mock_agent = MagicMock()
    mock_agent.chat_with_history.side_effect = Exception("Test error")

    with patch('src.tabs.vocab_tab.vocab_agent', mock_agent), \
         patch('src.tabs.vocab_tab.LOG') as mock_log:
        with pytest.raises(Exception) as exc_info:
            handle_vocab("Hello", [])
        assert str(exc_info.value) == "Test error"
