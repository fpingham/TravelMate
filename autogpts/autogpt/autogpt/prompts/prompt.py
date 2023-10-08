DEFAULT_TRIGGERING_PROMPT = (
    """
    Determine exactly one command to use next based on the given goals 
    and the progress you have made so far,
    and respond using the JSON schema specified previously.
    If doing a web search, you should strive to make it as directed as possible. Here are some guidelines to get the best results:
    - If you want to search for events, consider searching for 'eventbrite' links
    - If you want to search for general information, consider seraching for 'tripadvisor' forum discussions
    If doing a web search, you should choose the most promising results among the retrieved urls, using the search result body and title as reference.
    Also pay attention to the set goals and make sure your question is directly related to one of your goals
    You should ALWAYS base your responses on knowledge that you obtain from either
    You must ALWAYS start by loading the files that you have available in the directory.
    Try loading trip_details.pdf and tourist_profile.txt or any other file as well.
    user provided documents or the web:
    """
)

# If you previously made a google search and the selected webpage did not return interesting information,
# you can always try doing another fetch for one of the others