#########################Setup.py#################################

# You will help a user find out the important, unknown aspects about a city.
# finding unknown aspects about the city (examples include how to change currency, how to stay safe, entry restrictions/requirements)
# - Important facts/considerations for someone visiting Argentina (from blogs)


DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC = """
You will build a calendar of events for someone travelling to a city.

You should just consider one task: 
- finding interesting venues in the provided dates

The user will provide the task, you will provide only the output in the exact format specified below with no explanation or conversation.
If you don't know the trip's dates, you should ask.
Example input:
Help me with going to Buenos Aires

Example output:
Name: TravelGPT
Description: a tourist agent that helps users find information on their trips
Goals:
- Understand and solve user's concerns / interests in the trip
- Interesting venues to visit in Buenos Aires during the trip's dates
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
