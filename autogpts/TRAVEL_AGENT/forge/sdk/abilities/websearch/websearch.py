import json
import time
from itertools import islice

import requests
from duckduckgo_search import DDGS

from ..registry import ability

DUCKDUCKGO_MAX_ATTEMPTS = 3

@ability(
    name="google_search",
    description="Searches the web",
    parameters=[
        {
        "name": "query",
        "description": "google query",
        "type": "string",
        "required": True,
        }
    ],
    output_type="string",
  )

async def google_search(agent, task_id, query) -> str:
    """Return the results of a Google search

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.

    Returns:
        str: The results of the search.
    """
    search_results = []
    attempts = 0
    num_results = 8

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

    if isinstance(results, list):
        safe_message = json.dumps(
            [result.encode("utf-8", "ignore").decode("utf-8") for result in results]
        )
    else:
        safe_message = results.encode("utf-8", "ignore").decode("utf-8")
    return safe_message