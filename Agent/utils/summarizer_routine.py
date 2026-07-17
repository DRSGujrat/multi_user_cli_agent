from .summarizer import summarize
from ..database.UserDBSchema import SQLiteDB
from ..database.UserManager import UserManager
from ..database.MemoryManager import MemoryManager


db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)

inp = input("User Id : ")

if not um.user_exists(inp):
    print("User Does not exist.")

else:

    # Last summarized message id
    summary_track_id = mm.get_summary_track(inp)

    # Latest stored summary (returns list -> join into one string)
    previous_summary = "".join(
        mm.get_latest_summary(inp)
    )

    # Messages after the last summary checkpoint
    message_list = mm.get_messages_after(
        user_id=inp,
        message_id=summary_track_id,
    )

    if not message_list:
        print("Nothing new to summarize.")
        exit()

    # Latest message id in database
    last_message_id = mm.get_last_msg_id(inp)

    # Update summary instead of creating a new one
    updated_summary = summarize(
        previous_summary=previous_summary,
        messages=message_list,
    )

    mm.save_summary(
        user_id=inp,
        summary=updated_summary,
    )

    mm.update_summary_track(
        user_id=inp,
        message_id=last_message_id,
    )

    print("Summary updated successfully.")