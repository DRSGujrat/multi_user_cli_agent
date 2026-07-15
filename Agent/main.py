from .database.UserManager import UserManager
from .database.MemoryManager import MemoryManager
from .database.UserDBSchema import SQLiteDB
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from .database.SessionManager import SessionManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .models.model import model
from langchain_core.output_parsers import StrOutputParser
from .utils.summarizer import summarize



db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)
sm = SessionManager(um,mm)
parser = StrOutputParser()

um.delete_all_users()



while True:
    inp = input("Enter your username: ")
    
    if inp.lower() == "exit":
        break
    
    if not um.user_exists(inp):
        um.create_user(inp)

    session = sm.load_session(inp)
    session.conversation_summary = ''.join(session.conversation_summary)
    while True:

        query = input("Ask Anything...")

        if query.lower() == "exit":
            mm.add_all_messages(user_id = inp,  session_id=session.session_id, message_list=session.new_messages)
            break

        sm.append_message(session,message = HumanMessage(content = query))
        
        prompt = ChatPromptTemplate([
            SystemMessage(content = session.profile),
            HumanMessage(content = session.conversation_summary),
            MessagesPlaceholder("chat_history"),
            MessagesPlaceholder("new_conversation")
        ])
        
        chain = prompt | model | parser

        
        output = chain.invoke({'summary': session.conversation_summary,'chat_history' : session.recent_messages,"new_conversation" : session.new_messages})
        
        sm.append_message(session,AIMessage(content = output))
        print(output)


        if len(session.new_messages) == 10:
            session.conversation_summary = summarize(session.recent_messages)

            mm.save_summary(user_id = inp,summary = session.conversation_summary)
            session.recent_messages = session.new_messages.copy()
            session.new_messages.clear()
            
            mm.add_all_messages(session_id = session.session_id,user_id = inp,message_list=session.recent_messages)
            msg_id = mm.get_last_msg_id(inp)
            mm.update_summary_track(user_id = inp,message_id = msg_id)


        



