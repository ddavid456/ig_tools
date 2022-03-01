from instagram_private_api import Client
import random
import time


class ClearFollowers:

    def __init__(self, session: Client, safelist: list, users_to_delete:int = 5) -> None:
        self.session = session
        self.safelist = safelist
        self.users_to_delete = users_to_delete
        self._running = True

        self.runCommand()

    def runCommand(self):
        get_all_following = self.session.user_following(self.session.authenticated_user_id, self.session.uuid)
        print('Users Following', len(get_all_following['users']))

        users_to_unnfollow = [following['pk'] for following in get_all_following['users'] 
                            if following['username'] not in self.safelist]

        if len(users_to_unnfollow) < self.users_to_delete:
            self.users_to_delete = len(users_to_unnfollow) 

        for i in range(0,self.users_to_delete):
            print('Deleting: ', i+1)
            time.sleep(random.randrange(1,8))
            self.session.friendships_destroy(users_to_unnfollow[i])