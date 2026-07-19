from Agent.database.UserManager import UserManager
from Agent.database.MemoryManager import MemoryManager
from Agent.database.UserDBSchema import SQLiteDB
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from Agent.database.SessionManager import SessionManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from Agent.models.model import model
from langchain_core.output_parsers import StrOutputParser
from Agent.utils.summarizer import summarize


db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)
sm = SessionManager(um, mm)
parser = StrOutputParser()


while True:
    inp = input("Enter your username: ")
    if not inp.strip():
        print("Enter a valid user name")
        continue

    if inp.lower() == "exit":
        break

    if not um.user_exists(inp):
        um.create_user(inp)

    session = sm.load_session(inp)

    # Last few summaries fetched from DB -> convert list into one string
    print(session.conversation_summary)
    session.conversation_summary = "".join(session.conversation_summary)

    while True:
        query = input("Ask Anything... ")

        if query.lower() == "exit":
            if session.new_messages:
                mm.add_all_messages(
                    user_id=inp,
                    session_id=session.session_id,
                    message_list=session.new_messages,
                )

            break

        sm.append_message(session, HumanMessage(content=query))

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "{profile}"),
                ("system", "Previous Conversation Summary:\n{summary}"),
                MessagesPlaceholder("chat_history"),
                MessagesPlaceholder("new_conversation"),
            ]
        )

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
            print(f"Exception Occured: {e}")
            continue
        sm.append_message(session, AIMessage(content=output))

        print("AI :", output)

        # ---------------- SUMMARY ---------------- #

    if len(session.new_messages) >= 10:
        # Combine old short-term memory and current conversation
        summary_content = session.recent_messages + session.new_messages

        # Update summary using previous summary + new conversation

        session.conversation_summary = summarize(
            previous_summary=session.conversation_summary,
            messages=summary_content,
        )
        mm.save_summary(user_id=inp, summary=session.conversation_summary)

        mm.add_all_messages(
            session_id=session.session_id,
            user_id=inp,
            message_list=session.new_messages,
        )

        msg_id = mm.get_last_msg_id(inp)

        mm.update_summary_track(user_id=inp, message_id=msg_id)

        # New conversation becomes the next short-term memory
        session.recent_messages = session.new_messages.copy()

        session.new_messages.clear()
