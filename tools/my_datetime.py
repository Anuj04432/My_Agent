from langchain_core.tools import tool
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain.agents import create_agent


@tool
def get_datetime(query:str):
    """Provide an a current date and time"""
    now = datetime.now()
    return now

# llm = ChatOllama(model="qwen2.5:3b-instruct")

# agent = create_agent(model=llm, tools=[get_datetime],
#                      system_prompt= """When the user asks for the current date or time, "
#         "use the get_datetime tool. "
#         "Return the result in a clear format: 
#         {"date":
#         "timr":
#         }
#         """)

# response = agent.invoke({
#     "messages":{
#         "role":"user",
#         "content":"What is the current date and time"
#     }
# })

# print(response["messages"][-1].content)

