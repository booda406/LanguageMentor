import pytest
from unittest.mock import patch, MagicMock
import gradio as gr
from src.tabs.conversation_tab import create_conversation_tab, handle_conversation
from src.agents.conversation_agent import ConversationAgent

# Test handle_conversation function
def test_handle_conversation():
    # Mock ConversationAgent
    with patch('src.tabs.conversation_tab.conversation_agent') as mock_agent:
        # Setup the mock return value
        mock_agent.chat_with_history.return_value = "Hello, how can I help you?"

        # Test the function
        chat_history = []
        result = handle_conversation("Hi", chat_history)

        # Verify the results
        assert result == "Hello, how can I help you?"
        mock_agent.chat_with_history.assert_called_once_with("Hi")

# Test create_conversation_tab function
def test_create_conversation_tab():
    # Mock gradio components
    with patch('gradio.Markdown') as mock_markdown, \
         patch('gradio.Chatbot') as mock_chatbot, \
         patch('gradio.ChatInterface') as mock_chat_interface:

        # Setup mock returns
        mock_chatbot.return_value = MagicMock()
        mock_chat_interface.return_value = MagicMock()

        # Create a mock Tab context
        with patch('gradio.Tab') as mock_tab:
            # Call the function
            create_conversation_tab()

            # Verify that the components were created with correct parameters
            mock_markdown.assert_called_once_with("## 练习英语对话 ")

            mock_chatbot.assert_called_once_with(
                placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",
                height=800
            )

            # Verify ChatInterface was called with correct parameters
            mock_chat_interface.assert_called_once()
            call_args = mock_chat_interface.call_args[1]
            assert isinstance(call_args['fn'], type(handle_conversation))
            assert call_args['retry_btn'] is None
            assert call_args['undo_btn'] is None
            assert call_args['clear_btn'] == "清除历史记录"
            assert call_args['submit_btn'] == "发送"

# Test integration with ConversationAgent
def test_conversation_tab_integration():
    # Mock the ConversationAgent
    with patch('src.tabs.conversation_tab.conversation_agent') as mock_agent:
        # Setup mock response
        mock_agent.chat_with_history.return_value = "Test response"

        # Test handle_conversation integration
        chat_history = []
        result = handle_conversation("Test message", chat_history)

        # Verify integration
        assert result == "Test response"
        mock_agent.chat_with_history.assert_called_once_with("Test message")

# Test error handling
def test_handle_conversation_error():
    # Mock ConversationAgent with error
    with patch('src.tabs.conversation_tab.conversation_agent') as mock_agent:
        mock_agent.chat_with_history.side_effect = Exception("Test error")

        # Test the function with error
        chat_history = []
        with pytest.raises(Exception) as exc_info:
            handle_conversation("Hi", chat_history)

        assert str(exc_info.value) == "Test error"

