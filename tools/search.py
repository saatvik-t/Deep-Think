import os
from dotenv import load_dotenv
import logging
from tavily import TavilyClient

load_dotenv()

logger = logging.getLogger(__name__)

tavily_api = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(tavily_api)

def web_search(query : str) -> list :
    """
    Searches through the internet to fetch reliable information for a user query.
    Arguments:
        query (str): The question asked by the user.
    Return:
        list: The response as a list of JSONs.
    """
    logger.info(f"Query: {query}")
    results = tavily_client.search(query=query, max_results=5)

    # Response Format of Tavily Search Method
    # {
    #   "query": "",
    #   "answer": "",
    #   "images": [],
    #   "results": [
    #     {
    #       "url": "",
    #       "title": "",
    #       "content": "",
    #       "score": ,
    #       "raw_content": ,
    #     }
    #   ],
    #   "response_time": "1.67",
    #   "request_id": "123e4567-e89b-12d3-a456-426614174111"
    # }

    processed = []

    for result in results["results"]:
        page = {
            "title": result["title"],
            "url": result["url"],
            "score": result["score"]
        }
        processed.append(page)
        logger.info(page)

    processed.sort(key=lambda x: x["score"], reverse=True)
    return processed
