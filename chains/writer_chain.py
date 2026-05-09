import logging
from langchain_core.prompts import PromptTemplate
from langchain_groq.chat_models import ChatGroq
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

def format_documents(documents: list):
    """
    Formats documents into a clean, numbered context block.
    Arguments:
        documents (list): List containing the scraped content
    Returns:
        list: List of formatted strings containing the index, title and content of the document
        dict: Mapping the documents with their corresponding indices
    """
    logger.info(f"Formatting {len(documents)} documents")
    formatted_docs = []
    citation_map = {}

    for i, doc in enumerate(documents):
        if not doc["success"]:
            continue

        citation_map[i + 1] = {
            "source": i + 1,
            "title": doc["title"],
            "url": doc["url"]
        }

        content = doc["content"]
        formatted_docs.append(
            f"[{i+1}] {doc['title']}\n{content}"
        )

    logger.info("Formatting successful")
    return formatted_docs, citation_map

def build_writer_chain(writer_model, writer_prompt_file_path: str):
    """
    Initializes an LLM instance, fetches the prompt and builds the chain using LCEL.
    Arguments:
        writer_model (str): Model ID of the model to be used
        writer_prompt_file_path (str): Path to the file containing the prompt
    Returns:
        RunnableSerializable: The writer chain
    """
    writer_llm = ChatGroq(
        model=writer_model,
        temperature=0.3
    )
    logger.info("Building the Writer Chain")

    logger.info(f"Fetching the Prompt for Writer Chain from {writer_prompt_file_path}")
    with open(writer_prompt_file_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()
    logger.info("Fetched the Prompt for Writer Chain")
    writer_prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["query", "context"]
    )

    logger.info("Building the Writer Chain")
    writer_chain = (
        writer_prompt
        | writer_llm
        | StrOutputParser()
    )
    logger.info("Built the Writer Chain Successfully")

    return writer_chain

def run_writer_chain(writer_chain, query: str, documents: list) -> dict:
    """
    Generate answer based on the scraped documents.
    Arguments:
        writer_chain (RunnableSerializable): The writer chain
        query (str): The question asked by the user
        documents (list): List containing the scraped content
    Returns:
        dict: {"answer": str, "citations": dict}
    """
    logger.info("Running the Writer Chain")
    context, citation_map = format_documents(documents)

    logger.info("Invoking the Writer response")
    response = writer_chain.invoke({
        "query": query,
        "context": context
    })
    logger.info("Successfully fetched the response")
    logger.info(f"Response : {response}")
    logger.info(f"Citations : {citation_map}")

    return {
        "answer": response,
        "citations": citation_map
    }
