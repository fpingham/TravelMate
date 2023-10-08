from datetime import datetime

from autogpt.command_decorator import command


@command(
    "get_datetime",
    (
        "Use when you need to know the current date and time"
    ),
    {},
)

def get_datetime() -> str:
    """Return the current date and time

    Returns:
        str: The current date and time
    """
    return "Current date and time: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
