import pytest
from unittest.mock import patch, mock_open
from src.agents.conversation_agent import ConversationAgent
from langchain_core.messages import AIMessage

# Test the initialization of ConversationAgent
def test_conversation_agent_initialization():
    with patch("builtins.open", mock_open(read_data="This is a conversation prompt.")):
        agent = ConversationAgent()
        assert agent.name == "conversation"
        assert agent.prompt_file == "prompts/conversation_prompt.txt"
        assert agent.session_id == "conversation"

# Test if the ConversationAgent can handle a basic conversation
def test_conversation_handling():
    mock_prompt_content = "This is a conversation prompt."
    with patch("builtins.open", mock_open(read_data=mock_prompt_content)):
        with patch("src.agents.agent_base.RunnableWithMessageHistory.invoke", return_value=AIMessage(content="Hello, how can I help you?")):
            agent = ConversationAgent()
            response = agent.chat_with_history("Hi, what can you do?")
            assert response == "Hello, how can I help you?"

# Run the tests
if __name__ == "__main__":
    pytest.main()
