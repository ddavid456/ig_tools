from instagram_private_api import Client
import random
import json
import time
from typing import Union


class CreateSafelist:

    def __init__(self, session: Client, path: str):

        self.session = session
        self.path = path
        self._running = True

        self.runCommand()

    def runCommand(self):
        get_all_following = self.session.user_following(self.session.authenticated_user_id, self.session.uuid)
        current_following = [following['username'] for following in get_all_following['users']]

        # Clean up, updated followed json
        with open(self.path, 'w+') as file:
            file.write(json.dumps({"safeUsers": current_following}))
