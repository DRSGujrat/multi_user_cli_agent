from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage as HM, AIMessage as AM
from langchain_core.output_parsers import StrOutputParser
agent = create_agent(
    model = model, 
    tools = [web_search],
    )
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)


parser = StrOutputParser()
manager = UserManager()
manager.delete_every_user()
def ask_agent(user_id: str, query: str):
    
    if manager.is_user_present(user_id):
        manager.append_memory_message(user_id, HM(content=query))
    else:
        manager.create_user(user_id)
        
        user = UserProfile() 
        manager.append_memory_message(user_id, HM(content=query))
        
    
    user = manager.get_user_object(user_id)
    system_prompt_content = user.profile.to_prompt()
    
    
    template = ChatPromptTemplate([
        (
            'system', 
            "keep the answers concise and short, if the user is new then greet "
            "and be welcoming and helpful\n\n{system_profile}"
        ),
        MessagesPlaceholder(variable_name='chat_history')
    ])
    
    memory = manager.get_user_memory(user_id)
    chat_window = memory[-10:] if memory else []
    
    
    formatted_prompt = template.invoke({
        'system_profile': system_prompt_content,
        'chat_history': chat_window
    })
    
    
    response = agent.invoke({
        "messages": formatted_prompt.to_messages()
    })
    
    ai_message = response['messages'][-1]
    text = normalize_text(ai_message)
        
    
    manager.append_memory_message(user_id, AM(content=text))
    
    print(text)
    return response
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