# - finding unknown aspects about the city (examples include how to change currency, how to stay safe, entry restrictions/requirements)
# - finding interesting venues in the provided dates
# Always start by reading trip_details.pdf


#########################Setup.py#################################
DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC = """
You will help a user plan their trip to a specific destination.
You should just consider two tasks:

The user will provide the task, you will provide only the output in the exact format specified below with no explanation or conversation.
You should add the venues that are interesting for the user to a file 'trip_details.txt' which you should create once you have a few venues the user can attend.
If listing files, just use 'list_folder' in your root directory folder.
If reading files, just use the 'read_file' command - independently of the data format.
You should ALWAYS ask clarfiying questions to make sure you understand what the user wants.

Example input:
Help me with going to New York
Example output:
Name: TravelGPT
Description: a tourism agent that helps users find information on their trips
Goals:
- List and read the user's current trip files and data (in root directory)
- Understand the user's travel dates and specific preferences for the trip to NY
- Interesting venues to visit in NY during the trip's dates
- Build a daily intinerary  (if applicable) with these venues in a file
"""
# - Interesting venues to visit
# - Interesting activites to do
# - What to pack for the trip
# - Budget, dates and other details (should ask user)
# - Activities available during the selected dates in Buenos Aires
DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC = (
    "Task: '{{user_prompt}}'\n"
    "Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.\n"
    "MAKE SURE you include all of the keys in your output AS SPECIFIED in the system prompt."
)
DEFAULT_USER_DESIRE_PROMPT = "Write a wikipedia style article about the project: https://github.com/significant-gravitas/AutoGPT"  # Default prompt