import logging
from tools.search import web_search
from tools.scrape import scrape_search_results
from chains.writer_chain import build_writer_chain, run_writer_chain

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
            "documents": list,
            "answer": str,
            "citations": dict,
            "status": str
        }
    """
    logger.info("Running the Pipeline")
    state = {
        "query": topic,
        "search_results": [],
        "documents": [],
        "answer": "",
        "citations": "",
        "status": ""
    }

    state["search_results"] = web_search(topic)

    state["documents"] = scrape_search_results(state["search_results"])

    writer_chain = build_writer_chain(
        writer_model="meta-llama/llama-4-scout-17b-16e-instruct",
        writer_prompt_file_path="prompts/writer_prompt.txt"
    )
    writer_output = run_writer_chain(
        writer_chain=writer_chain,
        query=topic,
        documents=state["documents"]
    )
    state["answer"] = writer_output["answer"]
    state["citations"] = writer_output["citations"]

    state["status"] = "successful"

    logger.info("Pipeline executed successfully")
    return state
