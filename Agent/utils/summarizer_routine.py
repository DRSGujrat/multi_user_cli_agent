import asyncio

from fastapi import HTTPException

from Agent.database.MemoryManager import MemoryManager
from Agent.database.UserDBSchema import SQLiteDB
from Agent.database.UserManager import UserManager
from Agent.utils.summarizer import summarize

db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)


def summarizer_routine(user_id):

    inp = user_id

    if not um.user_exists(inp):
        raise HTTPException(status_code=404, detail="User Does not Exist")

    # Last summarized message id
    summary_track_id = mm.get_summary_track(inp)

    # Latest stored summary (returns list -> join into one string)
    summary = mm.get_latest_summary(inp)
    summary_text = []
    for sum in summary:
        summary_text.append(sum.content)
    previous_summary = "\n".join(summary_text)

    # Messages after the last summary checkpoint
    message_list = mm.get_messages_after(
        user_id=inp,
        message_id=summary_track_id,
    )

    if not message_list:
        return

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


summarizer_routine("DRS")
