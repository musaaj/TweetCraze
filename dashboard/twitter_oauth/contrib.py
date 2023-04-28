import logging
from tweepy import TweepyException
import uuid

logger = logging.getLogger(__name__)


class TwitterActions:
    last_accessed_follower = None
    last_accessed_tweet = None
    last_accessed_dm = None
    last_accessed_mention = None

    def __init__(self, twitter_api):
        if not twitter_api:
            raise ValueError("twitter_api must be an instance of TwitterAuthAPI")
        self.api = twitter_api

    def send_direct_message(self, twitter_user_id, msg):
        try:
            msg = f"{msg}\nMessage ID. {str(uuid.uuid4())}"
            self.api.send_direct_message(twitter_user_id, msg)
        except TweepyException as e:
            logger.exception(e)

    def send_bulk_direct_message(self, twitter_users_ids, msg):
        for user_id in twitter_users_ids:
            self.send_direct_message(user_id, msg)

    def get_followers(self, count=200):
        try:
            me = self.api.verify_credentials()
            return self.api.get_follower_ids(user_id=me.id, count=count)
        except TweepyException as e:
            logger.exception(e)
