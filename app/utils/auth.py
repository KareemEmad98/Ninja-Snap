from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

from app import Config


class OAuthHandler:
    def __init__(self):
        client = LegacyApplicationClient(client_id=Config.CLIENT_ID)
        self.oauth_session = OAuth2Session(client=client)
        self.refresh_access_token()

    def refresh_access_token(self):
        extra = {
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "refresh_token": Config.REFRESH_TOKEN,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        print(
            self.oauth_session.refresh_token(Config.TOKEN_URL, **extra, headers=headers)
        )

    def get_session_with_headers(self):
        access_token = self.oauth_session.token["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        self.oauth_session.headers.update(headers)
        return self.oauth_session
