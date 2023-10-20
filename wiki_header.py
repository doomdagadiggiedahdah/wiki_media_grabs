import requests
from markdownify import markdownify as md

def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = data["query"]["search"]
    return results

def get_wikipedia_intro(title):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "exintro": True,
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    return page["extract"]

def html_to_markdown(html):
    return md(html)

query = input("Enter your search query: \n")
results = search_wikipedia(query)
print("\n")
for i, result in enumerate(results):
    print(f"{i + 1}. {result['title']}")

selection = int(input("Enter the number of the page you want to view: \n"))
title = results[selection - 1]["title"]
intro_html = get_wikipedia_intro(title)
intro_markdown = html_to_markdown(intro_html)
print(intro_markdown)
