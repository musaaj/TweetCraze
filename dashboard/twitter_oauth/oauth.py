import logging
import tweepy
from tweepy import TweepyException
from django.conf import settings

logger = logging.getLogger(__name__)


class TwitterAuthAPI:
    def __init__(self, access_token=None, access_token_secret=None) -> None:
        self.auth = tweepy.OAuth1UserHandler(
            settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_KEY_SECRET
        )
        if access_token and access_token_secret:
            self.auth = tweepy.OAuth1UserHandler(
                settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_KEY_SECRET,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

    def authenticate(self, oauth_token, oauth_verifier):
        """Verify user authentication and return access_token and
        access_token_secret

        Args:
            oauth_token: oauth_token as return by callback url
            oauth_verifier: oauth_verifier as returned by the callback url

        Returns:
            tuple(access_token, access_token_secret,) on success else None
        """
        self.auth.request_token = {
            "oauth_token": oauth_token,
            "oauth_token_secret": oauth_verifier,
        }
        try:
            return self.auth.get_access_token(oauth_verifier)
        except TweepyException as e:
            logger.error(f"{str(e)}")
            return None

    @property
    def authorization_url(self):
        """get authorization url to allow user to authenticate our app by login
        to his twitter account
        """
        try:
            return self.auth.get_authorization_url(signin_with_twitter=True)
        except TweepyException as e:
            logger.error(f"{str(e)}")
            return None

    @property
    def API(self):
        """Get api handler for interacting with twitter endpoints

        Should only be called if this class was instanced with access_token and
        access_token_secret
        """
        try:
            return tweepy.API(self.auth)
        except TweepyException as e:
            logger.error(f"{str(e)}")
            return None
