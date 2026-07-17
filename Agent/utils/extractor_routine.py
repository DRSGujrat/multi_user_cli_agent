from .extractor import extract_user_profile
from ..database.UserDBSchema import SQLiteDB
from ..database.UserManager import UserManager
from ..database.MemoryManager import MemoryManager

from .merge_merge_unique import merge



db = SQLiteDB()
um = UserManager(db)
mm = MemoryManager(db)

inp = input("User Id : ")
if not um.user_exists(inp):
    print("User Does not exists")
else:
    profile_track_id = mm.get_profile_track(inp)

    message_list = mm.get_messages_after(
        user_id=inp,
        message_id=profile_track_id,
    )

    last_message_id = mm.get_last_msg_id(inp)

    new_profile = extract_user_profile(message_list)

    stored_profile = mm.get_latest_profile(inp)

    merge(
        stored_profile,
        new_profile,
    )

    mm.save_profile(
        user_id=inp,
        profile=new_profile,
    )

    mm.update_profile_track(
        user_id=inp,
        message_id=last_message_id,
    )