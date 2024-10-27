import pytest
from src.agents.session_history import get_session_history, store
from langchain_core.chat_history import InMemoryChatMessageHistory

def test_get_session_history_creates_new_instance():
    # Clear the store before testing
    store.clear()

    session_id = "test_session"
    history = get_session_history(session_id)

    # Check if a new instance of InMemoryChatMessageHistory is created
    assert isinstance(history, InMemoryChatMessageHistory)
    assert session_id in store
    assert store[session_id] is history

def test_get_session_history_retrieves_existing_instance():
    # Clear the store before testing
    store.clear()

    session_id = "test_session"
    # Manually create a session history
    store[session_id] = InMemoryChatMessageHistory()
    history = get_session_history(session_id)

    # Check if the existing instance is retrieved
    assert session_id in store
    assert store[session_id] is history

# Run the tests
if __name__ == "__main__":
    pytest.main()
