import logging
from tools.search import web_search
from tools.scrape import scrape_search_results

logger = logging.getLogger(__name__)

def run_pipeline(topic : str):
    """
    1. Search the user query to obtain a structured response.
    2. Scrapes all the URLs.
    3. Store the outputs in shared state
    Arguments:
        query (str): User question
    Returns:
        dict:
        {
            "query": str,
            "search_results": list,
            "documents": list
        }
    """
    logger.info("Running the Pipeline")
    state = {
        "query": topic,
        "search_results": [],
        "documents": []
    }

    state["search_results"] = web_search(topic)
    state["documents"] = scrape_search_results(state["search_results"])

    logger.info("Pipeline executed successfully")
    return state
