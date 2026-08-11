from langchain_core.messages import (
    BaseMessage,
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from Agent.models.model import model
from Agent.classes.UserProfile import UserProfileSchema
from fastapi import HTTPException

PROFILE_EXTRACTOR_SYSTEM_PROMPT = """You are an expert user profile extraction system.

Your task is to analyze the conversation and extract stable, long-term information about the user.

Extract only information that is explicitly stated or can be confidently inferred from repeated behavior in the conversation.

The output must conform exactly to the provided structured schema.

Guidelines:

- Extract only information relevant to the schema.
- Use concise phrases rather than complete sentences.
- Do not invent, guess, or assume information that is not supported by the conversation.
- Do not infer personal traits from a single casual statement unless it clearly represents a persistent preference or goal.
- Ignore temporary conversation context, greetings, jokes, or small talk.
- Ignore information about the assistant.
- If a field has no reliable information, leave it empty.
- Do not duplicate the same information across multiple fields unless it genuinely belongs in each.
- Merge semantically identical items into a single entry.
- Avoid redundant wording.

The profile should represent long-term knowledge that would remain useful in future conversations for personalizing responses."""


structured_model = model.with_structured_output(UserProfileSchema)


async def extract_user_profile(
    messages: list[BaseMessage],
) -> UserProfileSchema:
    """
    Extracts a structured user profile from a conversation.

    Parameters
    ----------
    messages : list[BaseMessage]
        Complete conversation history.

    Returns
    -------
    UserProfileSchema
        Extracted user profile.
    """

    filtered_messages: list[BaseMessage] = []

    for message in messages:
        # Ignore empty messages
        if not str(message.content).strip():
            continue

        # Ignore tool outputs
        if isinstance(message, ToolMessage):
            continue

        # Ignore empty AI messages generated for tool calls
        if (
            isinstance(message, AIMessage)
            and message.tool_calls
            and not str(message.content).strip()
        ):
            continue

        filtered_messages.append(message)

    prompt = [
        SystemMessage(content=PROFILE_EXTRACTOR_SYSTEM_PROMPT),
        *filtered_messages,
        HumanMessage(
            content=(
                "Extract the user's profile from this conversation. "
                "Return only the structured profile."
            )
        ),
    ]
    try:
        response = structured_model.invoke(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error : {e}")
    return response
