import os
import json
import random

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 导入提示模板相关类
from langchain_core.messages import HumanMessage, AIMessage  # 导入人类消息和 AI 消息类
from langchain_core.runnables.history import RunnableWithMessageHistory  # 导入带有消息历史的可运行类

from .session_history import get_session_history  # 导入会话历史相关方法
from utils.logger import LOG  # 导入日志工具
from config.language_models import AVAILABLE_MODELS


class ConversationAgent:
    """
    对话代理类，负责处理与用户的对话。
    """
    def __init__(self, session_id=None, model_name="gpt-4o-mini"):
        self.name = "conversation"  # 设置代理名称为 "conversation"
        self.session_id = session_id if session_id else self.name  # 如果未提供会话ID，则使用代理名称作为会话ID
        self.prompt_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'prompts', 'conversation_prompt.txt')
        self.prompt = ""
        self.load_prompt()

        self.model_name = model_name
        self.create_chatbot()  # 创建聊天机器人

    def load_prompt(self):
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as file:
                new_prompt = file.read().strip()
                if new_prompt != self.prompt:
                    print(f"檢測到提示詞變化：\n舊：{self.prompt[:100]}...\n新：{new_prompt[:100]}...")
                self.prompt = new_prompt
            if not self.prompt:
                raise ValueError("Prompt file is empty")
        except FileNotFoundError:
            print(f"Error: Prompt file not found at {self.prompt_file}")
            self.prompt = "Default conversation prompt"
        except Exception as e:
            print(f"Error loading prompt: {e}")
            self.prompt = "Default conversation prompt"


    def reload_prompt(self):
        """重新加載提示詞並重新初始化聊天機器人"""
        old_prompt = self.prompt
        self.load_prompt()
        if self.prompt != old_prompt:  # 只有當提示詞真的改變時才重新創建聊天機器人
            print("提示詞已更新，重新初始化聊天機器人...")
            self.create_chatbot()
            return True
        return False

    def create_chatbot(self):
        """
        初始化聊天机器人，包含系统提示和消息历史记录。
        """
        # 创建聊天提示模板，包括系统提示和消息占位符
        system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),  # 系统提示部分
            MessagesPlaceholder(variable_name="messages"),  # 消息占位符
        ])

        model = AVAILABLE_MODELS[self.model_name]()
        self.chatbot = system_prompt | model

        # 将聊天机器人与消息历史记录关联
        self.chatbot_with_history = RunnableWithMessageHistory(self.chatbot, get_session_history)


    def start_new_session(self):
        """
        开始一个新的聊天会话，发送初始的 AI 消息。
        """
        # 获取当前会话的历史记录
        history = get_session_history(self.session_id)
        LOG.debug(f"[history]:{history}")

        # 如果历史记录为空，则发送初始 AI 消息
        if not history.messages:
            initial_ai_message = "欢迎！今天有什么我能帮忙的吗？"  # 初始消息
            history.add_message(AIMessage(content=initial_ai_message))  # 将初始消息添加到历史记录
            return initial_ai_message
        else:
            return history.messages[-1].content  # 返回历史记录中的最后一条消息

    def chat_with_history(self, user_input):
        """
        处理用户输入，生成包含聊天历史的回复。
        
        参数:
            user_input (str): 用户输入的消息
        
        返回:
            str: AI 生成的回复
        """
        # 生成回复并考虑消息历史
        response = self.chatbot_with_history.invoke(
            [HumanMessage(content=user_input)],  # 将用户输入封装为 HumanMessage
            {"configurable": {"session_id": self.session_id}},  # 传入配置，包括会话ID
        )
        
        LOG.debug(response)  # 记录调试日志
        return response.content  # 返回生成的回复内容
