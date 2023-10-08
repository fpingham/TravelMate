"""Commands to search the web with"""

from __future__ import annotations

COMMAND_CATEGORY = "web_search"
COMMAND_CATEGORY_TITLE = "Web Search"

import subprocess

# Specify the library name you want to install
library_name = "langchain"

# Use subprocess to run the installation command
try:
    subprocess.check_call(["pip", "install", library_name])
    print(f"Successfully installed {library_name}")
except subprocess.CalledProcessError as e:
    print(f"Error installing {library_name}: {e}")

import json
import time
from itertools import islice

import openai
import requests
import tiktoken
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter

from autogpt.agents.agent import Agent
from autogpt.agents.utils.exceptions import ConfigurationError
from autogpt.command_decorator import command
from autogpt.core.utils.json_schema import JSONSchema

DUCKDUCKGO_MAX_ATTEMPTS = 3


@command(
  "fetch_webpage",
  "Retrieve the relevant content of a webpage related to specific topic",
  {
        "url": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The url to search for",
            required=True),
        "topic": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The type of information you want to extract from this url",
            required=True)
    },
)

def fetch_webpage(topic: str, url: str, agent: Agent) -> str:
    """Fetches a webpage"""
    # response = requests.get(url, timeout=5)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # all_text = soup.get_text()

    # print(all_text)

    loader = WebBaseLoader(url, header_template = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
    url_text = loader.load()  
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=3000, chunk_overlap=0
    )

    print(url_text)

    split_docs = text_splitter.split_documents(url_text)

    llm = ChatOpenAI(temperature=0)
    chain = load_summarize_chain(llm, chain_type="refine")

    chain.initial_llm_chain.prompt.template = 'From the following snippet, extract only the relevant aspects for' + topic + '\n\n\n"{text}"\n\n\nRELEVANT SNIPPETS:'
    chain.refine_llm_chain.prompt.template = "Your job is to produce a final collection of relevant snippets.\nWe have provided an existing summary up to a certain point: {existing_answer}\nWe have the opportunity to refine the existing summary (only if needed) with some more context below.\n------------\n{text}\n------------\nGiven the new context, refine the original summary, metioning ONLY the snippets relevant for " + topic + "\nIf the context isn't useful, return the original summary."

    res = chain.run(split_docs[:6])

    print(res)

    # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
    # res = encoding.encode(all_text.choices[0].text)
    # print('Number of tokens!!!')
    # print(len(res))
    # # import ipdb; ipdb.set_trace()

    return res

@command(
    "web_search",
    "Searches the web",
    {
        "query": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The search query",
            required=True,
        ),
    },
    aliases=["search"],
)
def web_search(query: str, agent: Agent, num_results: int = 6) -> str:
    """Return the results of a Google search

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """
    search_results = []
    attempts = 0

    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:
            return json.dumps(search_results)

        results = DDGS().text(query)
        search_results = list(islice(results, num_results))

        if search_results:
            break

        time.sleep(1)
        attempts += 1

    results = json.dumps(search_results, ensure_ascii=False, indent=4)
    return safe_google_results(results)


@command(
    "google",
    "Google Search",
    {
        "query": JSONSchema(
            type=JSONSchema.Type.STRING,
            description="The search query",
            required=True,
        )
    },
    lambda config: bool(config.google_api_key)
    and bool(config.google_custom_search_engine_id),
    "Configure google_api_key and custom_search_engine_id.",
    aliases=["search"],
)
def google(query: str, agent: Agent, num_results: int = 8) -> str | list[str]:
    """Return the results of a Google search using the official Google API

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """

    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    try:
        # Get the Google API key and Custom Search Engine ID from the config file
        api_key = agent.legacy_config.google_api_key
        custom_search_engine_id = agent.legacy_config.google_custom_search_engine_id

        # Initialize the Custom Search API service
        service = build("customsearch", "v1", developerKey=api_key)

        # Send the search query and retrieve the results
        result = (
            service.cse()
            .list(q=query, cx=custom_search_engine_id, num=num_results)
            .execute()
        )

        # Extract the search result items from the response
        search_results = result.get("items", [])

        # Create a list of only the URLs from the search results
        search_results_links = [item["link"] for item in search_results]

    except HttpError as e:
        # Handle errors in the API call
        error_details = json.loads(e.content.decode())

        # Check if the error is related to an invalid or missing API key
        if error_details.get("error", {}).get(
            "code"
        ) == 403 and "invalid API key" in error_details.get("error", {}).get(
            "message", ""
        ):
            raise ConfigurationError(
                "The provided Google API key is invalid or missing."
            )
        raise
    # google_result can be a list or a string depending on the search results

    # Return the list of search result URLs
    return safe_google_results(search_results_links)


def safe_google_results(results: str | list) -> str:
    """
        Return the results of a Google search in a safe format.

    Args:
        results (str | list): The search results.

    Returns:
        str: The results of the search.
    """
    if isinstance(results, list):
        safe_message = json.dumps(
            [result.encode("utf-8", "ignore").decode("utf-8") for result in results]
        )
    else:
        safe_message = results.encode("utf-8", "ignore").decode("utf-8")
    return safe_message
