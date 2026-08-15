import requests
from bs4 import BeautifulSoup

from langchain_core.tools import tool

@tool
def get_repos(query: str):
    """Get trending GitHub repositories based on the user's query."""
    url = "https://github.com/trending"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article", class_="Box-row")

    repos = []

    for article in articles:

        # Repository name and URL
        repo_link = article.find("h2").find("a")

        path = repo_link["href"].strip("/").split("/")
        owner = path[0]

        repo_name = repo_link.get_text(" ", strip=True)
        repo_url = "https://github.com" + repo_link["href"]
        

        # Description
        description_tag = article.find(
            "p",
            class_="col-9 color-fg-muted my-1 tmp-pr-4"
        )

        description = (
            description_tag.get_text(" ", strip=True)
            if description_tag
            else "No description"
        )

        # Programming language
        language_tag = article.find(
            "span",
            itemprop="programmingLanguage"
        )

        language = (
            language_tag.get_text(strip=True)
            if language_tag
            else "Unknown"
        )

        # Total stars
        star_link = article.find(
            "a",
            href=lambda x: x and "stargazers" in x
        )

        total_stars = (
            star_link.get_text(" ", strip=True)
            if star_link
            else "0"
        )

        # Stars today
        today_stars_tag = article.find(
            "span",
            class_="float-sm-right"
        )

        today_stars = (
            today_stars_tag.get_text(" ", strip=True)
            if today_stars_tag
            else "0 stars today"
        )

        repos.append({
        "owner": owner,
        "name": repo_name,
        "url": repo_url,
        "description": description,
        "language": language,
        "stars": total_stars,
        "stars_today": today_stars
    })

    return f"this are the trending repositories {repos}"


