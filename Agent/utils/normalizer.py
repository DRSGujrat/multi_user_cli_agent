from langchain_core.messages import AIMessage

def normalize_message(ai_message):

    if isinstance(ai_message.content, str):
        return ai_message

    text_parts = []

    for block in ai_message.content:
        if (
            isinstance(block, dict)
            and block.get("type") == "text"
        ):
            text_parts.append(block["text"])

    return AIMessage(
        content="\n".join(text_parts)
    )
