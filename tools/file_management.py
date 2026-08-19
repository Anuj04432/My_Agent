import os
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

@tool
def get_files(filename:str):
    """Find a file by its name anywhere on the C drive."""
    for root,directory,file in os.walk("C:\\"):
        if filename in file:
            path =  os.path.join(root,filename)
            return path

    return f"{filename} not found"

def get_folder(folder_name:str):
    for root,directory,file in os.walk("C:\\"):
        if folder_name in directory:
            path = os.path.join(root,folder_name)
            return path

def get_directory(folder,file):
    for root,dirs,files in os.walk("C:\\"):
        if folder in dirs:
            path = os.path.basename(root) == folder
            if file in files:
                return os.path.join(root,file)
    return "File not found"      


