from Agent.utils.extractor import extract_user_profile
from Agent.database.UserDBSchema import SQLiteDB
from Agent.database.UserManager import UserManager
from Agent.database.MemoryManager import MemoryManager

from Agent.utils.merge_merge_unique import merge

from fastapi import HTTPException

db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)


def extractor_routine(user_id):
    inp = user_id
    if not inp.strip():
        raise HTTPException(status_code=400, detail="User ID cannot be empty")
    if not um.user_exists(inp):
        raise HTTPException(status_code=404, detail="User does not exist")
    else:
        profile_track_id = mm.get_profile_track(user_id=inp)

        message_list = mm.get_messages_after(
            user_id=inp,
            message_id=profile_track_id,
        )
        if not message_list:
            return

        last_message_id = mm.get_last_msg_id(inp)

        new_profile = extract_user_profile(message_list)

        stored_profile = mm.get_latest_profile(inp)

        merge(
            stored_profile,
            new_profile,
        )

        mm.save_profile(
            user_id=inp,
            profile=stored_profile,
        )

        mm.update_profile_track(
            user_id=inp,
            message_id=last_message_id,
        )
