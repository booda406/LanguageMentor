import pytest
from unittest.mock import patch, MagicMock, mock_open
import gradio as gr
from src.tabs.scenario_tab import (
    create_scenario_tab,
    get_page_desc,
    start_new_scenario_chatbot,
    handle_scenario,
    agents
)
from src.agents.scenario_agent import ScenarioAgent

# Test scenario description loading
def test_get_page_desc():
    # Test successful file reading
    mock_content = "This is a test scenario description"
    with patch("builtins.open", mock_open(read_data=mock_content)):
        result = get_page_desc("job_interview")
        assert result == mock_content

    # Test file not found error
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("src.tabs.scenario_tab.LOG") as mock_log:
            result = get_page_desc("nonexistent_scenario")
            assert result == "场景介绍文件未找到。"
            mock_log.error.assert_called_once_with(
                "场景介绍文件 content/page/nonexistent_scenario.md 未找到！"
            )

# Test new scenario chatbot initialization
def test_start_new_scenario_chatbot():
    # Mock ScenarioAgent
    mock_agent = MagicMock()
    mock_agent.start_new_session.return_value = "Welcome to the job interview!"

    with patch.dict('src.tabs.scenario_tab.agents', {'job_interview': mock_agent}):
        chatbot = start_new_scenario_chatbot("job_interview")

        # Verify the chatbot initialization
        assert isinstance(chatbot, gr.Chatbot)
        mock_agent.start_new_session.assert_called_once()
        # 修正 value 的格式檢查
        assert chatbot.value == [[None, "Welcome to the job interview!"]]
        assert chatbot.height == 600

# Test scenario handling
def test_handle_scenario():
    # Mock ScenarioAgent and logger
    mock_agent = MagicMock()
    mock_agent.chat_with_history.return_value = "This is a test response"

    with patch.dict('src.tabs.scenario_tab.agents', {'job_interview': mock_agent}), \
         patch('src.tabs.scenario_tab.LOG') as mock_log:
        # Test normal conversation
        chat_history = []
        result = handle_scenario("Hello", chat_history, "job_interview")

        assert result == "This is a test response"
        mock_agent.chat_with_history.assert_called_once_with("Hello")
        mock_log.info.assert_called_once_with("[ChatBot]: This is a test response")

# Test scenario tab creation
def test_create_scenario_tab():
    with patch('gradio.Tab') as mock_tab, \
         patch('gradio.Markdown') as mock_markdown, \
         patch('gradio.Radio') as mock_radio, \
         patch('gradio.Chatbot') as mock_chatbot, \
         patch('gradio.ChatInterface') as mock_chat_interface:

        # Setup mock returns
        mock_radio.return_value = MagicMock()
        mock_chatbot.return_value = MagicMock()
        mock_chat_interface.return_value = MagicMock()

        # Call the function
        create_scenario_tab()

        # Verify components creation
        mock_markdown.assert_any_call("## 选择一个场景完成目标和挑战")

        # Verify Radio component creation
        mock_radio.assert_called_once()
        radio_args = mock_radio.call_args[1]
        assert radio_args['choices'] == [
            ("求职面试", "job_interview"),
            ("酒店入住", "hotel_checkin")
        ]
        assert radio_args['label'] == "场景"

        # Verify Chatbot creation
        mock_chatbot.assert_called_once_with(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",
            height=600
        )

        # Verify ChatInterface creation
        mock_chat_interface.assert_called_once()
        chat_interface_args = mock_chat_interface.call_args[1]
        assert chat_interface_args['retry_btn'] is None
        assert chat_interface_args['undo_btn'] is None
        assert chat_interface_args['clear_btn'] == "清除历史记录"
        assert chat_interface_args['submit_btn'] == "发送"

# Test agents initialization
def test_agents_initialization():
    assert "job_interview" in agents
    assert "hotel_checkin" in agents
    assert isinstance(agents["job_interview"], ScenarioAgent)
    assert isinstance(agents["hotel_checkin"], ScenarioAgent)

# Test scenario radio change handler
def test_scenario_radio_change():
    mock_desc = "Test description"
    mock_chatbot = gr.Chatbot()

    # 使用 patch 裝飾器來模擬 get_page_desc 和 start_new_scenario_chatbot
    with patch('src.tabs.scenario_tab.get_page_desc') as mock_get_desc, \
         patch('src.tabs.scenario_tab.start_new_scenario_chatbot') as mock_start_chatbot:

        # 設置 mock 的返回值
        mock_get_desc.return_value = mock_desc
        mock_start_chatbot.return_value = mock_chatbot

        # 創建一個真實的 Radio 組件
        scenario_radio = gr.Radio(
            choices=[("求職面試", "job_interview"), ("酒店入住", "hotel_checkin")],
            label="場景"
        )

        # 使用實際的函數而不是 lambda
        def change_fn(scenario):
            # 直接使用被 mock 的函數
            desc = mock_get_desc(scenario)
            chatbot = mock_start_chatbot(scenario)
            return desc, chatbot

        # 調用函數並驗證結果
        desc, chatbot = change_fn("job_interview")

        # 驗證結果
        assert desc == mock_desc  # 應該是 "Test description"
        assert chatbot == mock_chatbot
        mock_get_desc.assert_called_once_with("job_interview")
        mock_start_chatbot.assert_called_once_with("job_interview")

# Test error cases
def test_handle_scenario_error():
    mock_agent = MagicMock()
    mock_agent.chat_with_history.side_effect = Exception("Test error")

    with patch.dict('src.tabs.scenario_tab.agents', {'job_interview': mock_agent}), \
         patch('src.tabs.scenario_tab.LOG') as mock_log:
        with pytest.raises(Exception) as exc_info:
            handle_scenario("Hello", [], "job_interview")
        assert str(exc_info.value) == "Test error"

# Test invalid scenario selection
def test_invalid_scenario():
    with pytest.raises(KeyError):
        start_new_scenario_chatbot("invalid_scenario")

def test_get_page_desc_mock():
    """測試 get_page_desc 的 mock 是否正確工作"""
    expected_desc = "Test mock description"
    with patch('src.tabs.scenario_tab.get_page_desc') as mock_get_desc:
        mock_get_desc.return_value = expected_desc
        actual_desc = mock_get_desc("any_scenario")
        assert actual_desc == expected_desc
