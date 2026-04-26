import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def scrape_url(url: str) -> dict:
    """
    Scrapes and cleans the textual content from a given URL.
    Arguments:
        url (str): Webpage URL
    Returns:
        dict: {"url": str, "domain": str, "content": str, "success": bool, "error": str | None}
    """
    try:
        logger.info(f"Scraping URL: {url}")
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "form", "svg"]):
            tag.decompose()

        main_content = soup.get_text(separator=" ", strip=True)
        cleaned_text = " ".join(main_content.split())

        result = {
            "url": url,
            "domain": urlparse(url).netloc,
            "content": cleaned_text,
            "success": True,
            "error": None
        }
        logger.info(f"Successfully scraped URL: {url}")
        return result

    except requests.exceptions.Timeout:
        logger.warning(f"Timeout while scraping URL: {url}")
        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "content": "",
            "success": False,
            "error": "Timeout occurred"
        }

    except requests.exceptions.RequestException as e:
        logger.warning(f"Request failed for {url}: {str(e)}")
        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "content": "",
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

    except Exception as e:
        logger.exception(f"Unexpected scraping error for {url}: {str(e)}")
        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "content": "",
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }

def scrape_search_results(search_results: list) -> list:
    """
    Scrapes multiple URLs from Tavily search output.
    Arguments:
        search_results (list): Output from web_search
    Returns:
        list: List of dictionaries from the contents of scrape_url()
    """
    logger.info(f"Scraping all URLs")

    documents = []
    for result in search_results:
        scraped = scrape_url(result["url"])

        doc = {
            "url": result["url"],
            "domain": scraped["domain"],
            "title": result["title"],
            "content": scraped["content"],
            "success": scraped["success"],
            "error": scraped["error"],
            "score": result["score"]
        }
        documents.append(doc)

    documents.sort(
        key=lambda x: (x["success"], x["score"]),
        reverse=True
    )

    logger.info("Scraped all URLs")
