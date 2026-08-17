from langchain_core.tools import tool
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


@tool
def get_datetime(query:str):
    """Provide an a current date and time"""
    now = datetime.now()
    return now

