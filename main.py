from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools.get_weather import get_weather
from tools.my_datetime import get_datetime
from tools.file_management import create_file,get_directory,get_files,get_folder,delete_file
llm = ChatOllama(model="qwen2.5:3b-instruct")

agent = create_agent(
    model=llm,
    tools=[get_weather, get_datetime,get_files, get_folder, get_directory, create_file, delete_file],
    system_prompt = """
You are a helpful assistant with access to weather, datetime, and file-management tools.

Rules:

1. Weather:
- If the user asks about weather or temperature, use the get_weather tool.
- Format the weather result as:
  Temperature: <temperature>
  City: <city>
  Condition: <condition>

2. Date and Time:
- If the user asks for the current date or time, use the get_datetime tool.
- Format the result as:
  Date: <date>
  Time: <time>

3. File Management:
- If the user asks for the location of a file, use the get_files tool.
- If the user asks for the location of a folder, use the get_folder tool.
- If the user asks for a specific file inside a particular folder, use the get_directory tool.
- If the user asks to create a file, use the create_file tool.
- If the user asks to delete a file, use the delete_file tool.
- Never guess a file or folder location. Always use the appropriate tool.
- When returning a file or folder location, provide the absolute path.
- Before creating a file, make sure you do not overwrite an existing file unless the user explicitly asks you to overwrite it.
- Before deleting a file, verify that the file exists.
- Report the result of every file operation clearly.

4. Multiple Questions:
- If the user asks multiple questions, answer ALL parts of the question.
- Use the appropriate tools for each part when necessary.
- Do not ignore any part of the user's question.

5. Other Questions:
- If the question does not require a tool, answer using your normal knowledge.
- Do not ignore any part of the user's question.

6. Tool Usage:
- Always use the appropriate tool when the user's request requires real-time information or file operations.
- Do not fabricate tool results.
- After receiving a tool result, use that result to formulate the final answer.
"""
)
query = input("Enter the prompt:")
response = agent.invoke({
    "messages":{
        "role":"user",
        "content":query
    }
})


print(response["messages"][-1].content)