from instagram_private_api import Client
import random
import time
import re

class deleteComments:

    def __init__(self, session: Client, patterns: list, lastposts: int) -> None:
        self.session = session
        self.patterns = patterns
        self.lastposts = lastposts
        self._running = True

        self.runCommand()


    def runCommand(self):
        """
        Data structure for post/comments
        {
            "post_id": {
                "comments": [(text, comment_id),....],
                "delete_ids": [comment_id]
            }
        }
        
        """
        comment_data = {}

        try:
            search_patterns = [re.compile(pattern) for pattern in self.patterns]
        except:
            print('Issue compiling patterns')
            return

        self_feed = self.session.self_feed()

        self.lastposts = len(self_feed['items']) if len(self_feed['items']) < self.lastposts  else  self.lastposts

        last_n_posts = [post['pk'] for post in self_feed['items'][:self.lastposts]]

        # Only goes through top level of comments
        # Future need it to trunk into comment replies
        for post_id in last_n_posts:
            comments = (self.session.media_comments(post_id))
