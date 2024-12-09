import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from pathlib import Path
path = Path(myDir)
a=str(path.parent.absolute())

sys.path.append(a)

from src.database.db import init_db
from src.database.crud import UserManager
from src.chatbot.main import bot_loop
from src.utils import fill_db_with_participants, draw_wishlists, send_welcome_message, send_decision_message

if __name__ == '__main__':
    init_db()
    # fill_db_with_participants()
    # send_welcome_message()
    # bot_loop()
    # draw_wishlists()
    # send_decision_message()
