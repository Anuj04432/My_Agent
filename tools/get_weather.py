from langchain_core.tools import tool 
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import requests
import os
from dotenv import load_dotenv
load_dotenv()


@tool
def get_weather(city:str):
    """Whats the weather in city"""
    api_key = os.getenv("WEATHER_API_KEY")
    url = "http://api.weatherapi.com/v1/current.json"
    params ={
        "key":api_key,
        "q":city
    }

    data = requests.get(url,params=params)
    response =  data.json()

    return response



llm = ChatOllama(model="qwen2.5:3b-instruct")

agent = create_agent(model=llm,
                     tools=[get_weather],
                     system_prompt="Give only the temparature and city name with condition no wxtra details"
                     )

response = agent.invoke({
    "messages":{
        "role":"user",
        "content":"What is the weather in kolkatta"
    }
})


print(response["messages"][-1].content)