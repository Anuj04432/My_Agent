from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools.get_weather import get_weather
from tools.my_datetime import get_datetime

llm = ChatOllama(model="qwen2.5:3b-instruct")

agent = create_agent(
    model=llm,
    tools=[get_weather, get_datetime],
    system_prompt="""
You are a helpful assistant with access to weather and datetime tools.

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

3. Multiple questions:
- If the user asks multiple questions, answer ALL parts of the question.
- Use the appropriate tools for each part when necessary.

4. Other questions:
- If the question does not require a tool, answer using your normal knowledge.
- Do not ignore any part of the user's question.

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