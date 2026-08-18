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

llm = ChatOllama(model="qwen2.5:3b-instruct")

agent = create_agent(
    model=llm,
    tools=[get_files],
    system_prompt = """
You are a file management assistant.

Use the available tools to find, create, move, copy, or delete files and folders.

When the user asks to find a file, use the file search tool.
When the user asks to find a folder, use the folder search tool.

Always give the full path of the file or folder.
""")

query = input("Enter the prompt:")
response = agent.invoke({
    "messages":{
        "role":"user",
        "content":query
    }
})


print(response["messages"][-1].content)