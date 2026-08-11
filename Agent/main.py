import asyncio
import time

from fastapi import FastAPI, HTTPException
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from Agent.database.MemoryManager import MemoryManager
from Agent.database.SessionManager import SessionManager
from Agent.database.UserDBSchema import SQLiteDB
from Agent.database.UserManager import UserManager
from Agent.models.model import model
from Agent.utils.summarizer import summarize

app = FastAPI()

db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)
sm = SessionManager(um, mm)
parser = StrOutputParser()


@app.post("/chat/{username}")
async def chat(username: str, user_query: str):
    start = time.perf_counter()

    inp = username
    if not inp.strip():
        raise HTTPException(status_code=400, detail="User name cannot be empty")

    if not um.user_exists(inp):
        um.create_user(inp)

    session = sm.load_session(inp)

    # Last few summaries fetched from DB -> convert list into one string

    session.conversation_summary = "\n".join(session.conversation_summary)

    query = user_query
    if not query.strip():
        raise HTTPException(status_code=400, detail="User query cannot be empty")

    sm.append_message(session, HumanMessage(content=query))

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{profile}"),
            ("system", "Previous Conversation Summary:\n{summary}"),
            MessagesPlaceholder("chat_history"),
            MessagesPlaceholder("new_conversation"),
        ]
    )
    print(f"Pass Summary : {session.conversation_summary}")
    print(f"Passed History : {session.recent_messages}")
    print(f"Passed Profile: {session.profile}")
    print(f"Passed Conversation : {session.new_messages}")
    llm_start = time.perf_counter()
    chain = prompt | model | parser
    try:
        output = chain.invoke(
            {
                "profile": session.profile,
                "summary": session.conversation_summary,
                "chat_history": session.recent_messages,
                "new_conversation": session.new_messages,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {e}")
    llm_end = time.perf_counter()
    sm.append_message(session, AIMessage(content=output))

    # # ---------------- SUMMARY ---------------- #

    # if len(session.new_messages) >= 10:
    #     # Combine old short-term memory and current conversation
    #     summary_content = session.recent_messages + session.new_messages

    #     # Update summary using previous summary + new conversation

    #     summary = asyncio.create_task(
    #         summarize(
    #             previous_summary=session.conversation_summary,
    #             messages=summary_content,
    #         )
    #     )
    #     session.conversation_summary = await summary
    #     await mm.save_summary(user_id=inp, summary=session.conversation_summary)

    mm.add_all_messages(
        session_id=session.session_id,
        user_id=inp,
        message_list=session.new_messages,
    )

    #     msg_id = await mm.get_last_msg_id(inp)

    #     await mm.update_summary_track(user_id=inp, message_id=msg_id)

    #     # New conversation becomes the next short-term memory
    #     session.recent_messages = session.new_messages.copy()

    #     session.new_messages.clear()
    end = time.perf_counter()
    print(f"Start to end Latency : {end - start:.3f} sec")
    print(f"LLM Latency: {llm_end - llm_start:.3f} sec")
    return {"messages": output}
