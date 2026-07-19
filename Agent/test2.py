# This file is for testinn purposes only

from .database.UserManager import UserManager
from .database.MemoryManager import MemoryManager
from .database.UserDBSchema import SQLiteDB
from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from .database.SessionManager import SessionManager
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .models.model import model
from langchain_core.output_parsers import StrOutputParser
from .utils.summarizer import summarize
from .classes.UserProfile import UserProfile



db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)
sm = SessionManager(um,mm)
parser = StrOutputParser()



inp = 'test'
# msg_id = mm.get_last_msg_id(inp)

# print(msg_id)
# mm.save_summary(user_id=inp,summary = 'summarized')
# mm.update_summary_track(user_id = inp,message_id =msg_id)
# u1 = UserProfile()
# mm.save_profile(user_id = inp,profile = u1)
# mm.update_profile_track(user_id=inp,message_id = msg_id)

# messages = mm.get_all_messages(inp)
# summary = mm.get_latest_summary(user_id = inp)

# for msg in messages:
#     if isinstance(msg,HumanMessage):
#         print("User :",msg.content)
#     elif isinstance(msg,AIMessage):
#         print("AI :",msg.content)

# print("Summary : ",summary[0].content)

# profile = mm.get_latest_profile(user_id = inp)
# print(profile)

mm.delete_latest_profile(user_id = inp)

