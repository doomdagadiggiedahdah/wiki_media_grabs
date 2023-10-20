import requests
from markdownify import markdownify as md

def search_wiktionary(query):
    url = "https://en.wiktionary.org/w/api.php"
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

def get_wiktionary_sections(title):
    url = "https://en.wiktionary.org/w/api.php"
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "sections",
    }
    response = requests.get(url, params=params)
    data = response.json()
    sections = data["parse"]["sections"]
    return sections

def get_wiktionary_etymology(title):
    sections = get_wiktionary_sections(title)
    etymology_section = next((section for section in sections if section["line"] == "Etymology"), None)
    if etymology_section is None:
        return "No etymology section found."
    section_number = etymology_section["index"]
    url = "https://en.wiktionary.org/w/api.php"
    params = {
        "action": "parse",
        "format": "json",
        "page": title,
        "section": section_number,
        "prop": "text",
    }
    response = requests.get(url, params=params)
    data = response.json()
    text = data["parse"]["text"]["*"]
    return text

def html_to_markdown(html):
    return md(html)

query = input("Enter your search query: ")
results = search_wiktionary(query)
for i, result in enumerate(results):
    print(f"{i + 1}. {result['title']}")

selection = int(input("Enter the number of the page you want to view: "))
title = results[selection - 1]["title"]
etymology_html = get_wiktionary_etymology(title)
etymology_markdown = html_to_markdown(etymology_html)
print(etymology_markdown)
