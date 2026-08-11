from langchain_core.tools import tool 
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import requests
import os
from dotenv import load_dotenv
load_dotenv()

@tool
def get_news(query:str):
    """Fetch the latest news related to the given query"""

    api_key = os.getenv("NEWS_API_KEY")

    if not api_key:
        return "the api is not connected"

    url = f"https://newsdata.io/api/1/latest"
    params = {"apikey":api_key,
              "q":query,
              "country":"in",
              "language":"en"
              }


    response = requests.get(url=url,params=params)
    data = response.json()
    article =  data["results"]
    if not article:
        return "No articles were found"

    news = []
    for article in article:
        news.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "date": article.get("pubDate"),
            "source": article.get("source_name"),
            "link": article.get("link")
        })

    return news


llm = ChatOllama(model="qwen2.5:3b-instruct")

agent = create_agent(model=llm,
                     tools=[get_news],
                     system_prompt="""You are an AI news assistant.

When the user asks for current AI news:
1. Use the get_news tool.
2. Focus only on Artificial Intelligence news.
3. Prefer news related to India when requested.
4. Return a maximum of 10 headlines.
5. For each article include:
   - Headline
   - Short summary
   - Date
   - Source
6. Do not invent news or dates.
7. If there is no relevant news, say so clearly.
""")

response = agent.invoke({
    "messages":{
        "role":"user",
        "content":"What is current ai news of ai in india?"
    }
})


print(response["messages"][-1].content)