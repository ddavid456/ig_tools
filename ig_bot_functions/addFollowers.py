from instagram_private_api import Client
import random
import json
import time
from typing import Union

class AddFollowers:

    def __init__(self, session: Client,
                       amount: int = 300, 
                       user_to_target: Union[str, None] = None) -> None:

        self.session = session
        self.amount = amount
        self.followed = {}
        self.user_to_target = user_to_target
        self._running = True

        self.runCommand()

    def runCommand(self):
        get_all_following = self.session.user_following(self.session.authenticated_user_id, self.session.uuid)
        current_following = [following['username'] for following in get_all_following['users']]
        time.sleep(2)
        # Load Followed list
        with open('config/followed.json') as file:
            self.followed = json.load(file)

        if self.user_to_target:
            # Get all followers from user
            get_all_followers = []
            user_id = self.session.search_users(self.user_to_target)['users'][0]['pk']
            time.sleep(random.randrange(2,4))
            rank_token = self.session.generate_uuid()
            results = self.session.user_followers(user_id, rank_token)
            get_all_followers.extend(results.get('users', []))

            next_max_id = results.get('next_max_id')
            while next_max_id and len(get_all_followers) < 10000:
                time.sleep(random.randrange(2,8))
                print(len(get_all_followers))
                results = self.session.user_followers(user_id, rank_token, max_id=next_max_id)
                get_all_followers.extend(results.get('users', []))
                next_max_id = results.get('next_max_id')

            print(len(get_all_followers))
            users_to_follow = [follow['pk'] for follow in get_all_followers if follow['pk'] not in self.followed['followed'] and follow['username'] not in current_following]

        if not self.user_to_target:
            new_target = get_all_following['users'][random.randrange(0, len(get_all_following['users']))]
            print('Targeting: ', new_target['username'])
            get_all_followers = self.session.user_followers(new_target['pk'], self.session.generate_uuid())
            users_to_follow = [follow['pk'] for follow in get_all_followers['users'] if follow['pk'] not in self.followed['followed']]

        print(len(users_to_follow))
        if len(users_to_follow) < self.amount:
            self.amount = len(users_to_follow) 

        try:
            for i in range(0,self.amount):
                print('Adding: ', i+1)
                time.sleep(random.randrange(2,18))
                self.followed['followed'].append(users_to_follow[i])
                self.session.friendships_create(users_to_follow[i])
        except Exception as e:
            print('Error adding users, please try again later.')
            print(e)
            

        # Clean up, updated followed json
        with open('config/followed.json', 'w') as file:
            file.write(json.dumps(self.followed))
