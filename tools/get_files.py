from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

import os


# @tool
# def delete_file():
#     file = input("Enter the file name: ")
#     if os.path.exists(file):
#         os.remove(file)
#         return f"{file} file deleted"
#     else:
#         return f"{file} file not exist"

@tool
def create_file(filename: str, content: str):
    """Create a file and write the content"""
    if os.path.exists(filename):
          return f"{filename} file already exists"
    with open(filename,"w", encoding='utf-8') as f:
                f.write(content)

    return f"{filename} file has created successfully"
        
llm = ChatOllama(model="qwen2.5:3b-instruct")

agent = create_agent(
    model=llm,
    tools=[create_file],
    system_prompt = """
You are a helpful Python File Handling Agent.

Your job is to help users create files.

When the user asks to create a file:
1. Identify the filename.
2. Identify the content.
3. Call the create_file tool.
4. Tell the user whether the file was created successfully.

Keep responses short and practical.
""" )

query = input("Enter the prompt:")
response = agent.invoke({
    "messages":{
        "role":"user",
        "content":query
    }
})


print(response["messages"][-1].content)
    
    
