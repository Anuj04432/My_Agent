from langchain_core.tools import tool 
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
