# making search tool which is searching in google

from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name: str):
    """Searched for LinkedIn or Twitter Profile page."""
    # create an object
    search = TavilySearchResults()
    res = search.run(f"{name}")

    return res