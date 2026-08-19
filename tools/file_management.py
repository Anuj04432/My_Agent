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
        
        if os.path.basename(root) == folder:
            if file in files:
                return os.path.join(root,file)
    return "File not found"      

def create_file(filename: str, content: str):
    """Create a file and write the content"""
    if os.path.exists(filename):
          return f"{filename} file already exists"
    with open(filename,"w", encoding='utf-8') as f:
                f.write(content)

    return f"{filename} file has created successfully"

def delete_file():
    file = input("Enter the file name: ")
    if os.path.exists(file):
        os.remove(file)
        return f"{file} file deleted"
    else:
        return f"{file} file not exist"

print(get_directory("tools", "git_tool.py"))