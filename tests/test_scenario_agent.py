import pytest
from unittest.mock import patch, mock_open
import json
from src.agents.scenario_agent import ScenarioAgent
from langchain_core.messages import AIMessage

# Test the initialization of ScenarioAgent
def test_scenario_agent_initialization():
    scenario_name = "test_scenario"
    valid_json_content = json.dumps(["Welcome to the scenario!"])  # Ensure this is valid JSON
    with patch("builtins.open", mock_open(read_data="This is a test prompt.")), \
         patch("json.load", return_value=json.loads(valid_json_content)):
        agent = ScenarioAgent(scenario_name=scenario_name)
        assert agent.name == scenario_name
        assert agent.prompt_file == f"prompts/{scenario_name}_prompt.txt"
        assert agent.intro_file == f"content/intro/{scenario_name}.json"
        assert agent.session_id == scenario_name

# Test starting a new session with ScenarioAgent
def test_start_new_session():
    scenario_name = "test_scenario"
    valid_json_content = json.dumps(["Welcome to the scenario!"])  # Ensure this is valid JSON
    with patch("builtins.open", mock_open(read_data="This is a test prompt.")), \
         patch("json.load", return_value=json.loads(valid_json_content)):
        with patch("src.agents.scenario_agent.get_session_history") as mock_get_session_history:
            mock_get_session_history.return_value.messages = []
            agent = ScenarioAgent(scenario_name=scenario_name)
            initial_message = agent.start_new_session()
            assert initial_message == "Welcome to the scenario!"

# Test starting a new session with existing history
def test_start_new_session_with_history():
    scenario_name = "test_scenario"
    valid_json_content = json.dumps(["Welcome to the scenario!"])  # Ensure this is valid JSON
    with patch("builtins.open", mock_open(read_data="This is a test prompt.")), \
         patch("json.load", return_value=json.loads(valid_json_content)):
        with patch("src.agents.scenario_agent.get_session_history") as mock_get_session_history:
            mock_get_session_history.return_value.messages = [AIMessage(content="Previous message")]
            agent = ScenarioAgent(scenario_name=scenario_name)
            last_message = agent.start_new_session()
            assert last_message == "Previous message"

# Run the tests
if __name__ == "__main__":
    pytest.main()
