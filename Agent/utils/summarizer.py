from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.output_parsers import StrOutputParser

from fastapi import HTTPException
from ..models.model import model


SUMMARIZER_SYSTEM_PROMPT = """
You are an expert conversation summarizer.

You will receive:

1. A previous conversation summary.
2. A new chunk of conversation.

Your task is to UPDATE the summary.

Requirements:

- Preserve important information from the previous summary.
- Incorporate new important information from the latest conversation.
- Remove duplicate information.
- Keep the summary concise but information-rich.

Preserve:

- User goals
- User preferences
- Important facts shared by the user
- Decisions made
- Important AI responses
- Ongoing tasks
- Future action items
- Useful long-term context

Ignore:

- Greetings
- Repeated information
- Tool execution details
- Empty messages
- Conversation noise

Return only the updated summary.
"""

parser = StrOutputParser()


async def summarize(
    previous_summary: str,
    messages: list[BaseMessage],
) -> str:
    """
    Updates the conversation summary.

    Parameters
    ----------
    previous_summary : str
        Previously stored conversation summary.

    messages : list[BaseMessage]
        New conversation chunk to merge into the summary.

    Returns
    -------
    str
        Updated summary.
    """

    filtered_messages = []

    for message in messages:
        # Ignore empty messages
        if not str(message.content).strip():
            continue

        # Ignore tool messages
        if isinstance(message, ToolMessage):
            continue

        # Ignore empty AI tool-call messages
        if (
            isinstance(message, AIMessage)
            and message.tool_calls
            and not str(message.content).strip()
        ):
            continue

        filtered_messages.append(message)

    prompt = [
        SystemMessage(content=SUMMARIZER_SYSTEM_PROMPT),
        SystemMessage(
            content=f"""
            Previous Conversation Summary:

            {previous_summary if previous_summary else "No previous summary available."}
        """
        ),
        *filtered_messages,
        HumanMessage(
            content=(
                "Update the previous summary using the new conversation. "
                "Do not lose important information already present in the previous summary."
            )
        ),
    ]
    try:
        response = await model.ainvoke(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error : {e}")

    return parser.invoke(response).strip()
