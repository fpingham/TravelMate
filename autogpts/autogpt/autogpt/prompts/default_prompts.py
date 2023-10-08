#########################Setup.py#################################

DEFAULT_SYSTEM_PROMPT_AICONFIG_AUTOMATIC = """
You will help a user with his tourism goals.
You will generate a plan of 1 steps and then you are going to ask the user where he feels you should get started.
The user will prompt you with questions and you will answer.

The user will provide the task, you will provide only the output in the exact format specified below with no explanation or conversation.

Example input:
Help me with going to Buenos Aires

Example output:
Name: TravelGPT
Description: a tourist agent that helps users find information on their trips
Goals:
- Travel considerations (not government, more general like blogs from other travellers) involved when travelling to Buenos Aires
"""

# - Budget, dates and other details (should ask user)

# - Activities available during the selected dates in Buenos Aires

DEFAULT_TASK_PROMPT_AICONFIG_AUTOMATIC = (
    "Task: '{{user_prompt}}'\n"
    "Respond only with the output in the exact format specified in the system prompt, with no explanation or conversation.\n"
)

DEFAULT_USER_DESIRE_PROMPT = "Write a wikipedia style article about the project: https://github.com/significant-gravitas/AutoGPT"  # Default prompt
