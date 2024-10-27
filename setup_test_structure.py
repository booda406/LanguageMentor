import os

# 定義要建立的資料夾和檔案結構
test_structure = {
    "tests": [
        "test_agent_base.py",
        "test_conversation_agent.py",
        "test_scenario_agent.py",
        "test_session_history.py",
        "test_vocab_agent.py",
        "test_conversation_tab.py",
        "test_scenario_tab.py",
        "test_vocab_tab.py"
    ]
}

def create_structure(base_path, structure):
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'w') as f:
                f.write("# This is a placeholder for {}\n".format(file))

# 執行腳本，在專案根目錄下建立結構
if __name__ == "__main__":
    base_directory = '.'  # 根據需要調整基準目錄
    create_structure(base_directory, test_structure)
    print("Test folder and files created successfully.")

