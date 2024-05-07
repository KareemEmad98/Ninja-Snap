class Config:
    SQLALCHEMY_DATABASE_URI:str = 'sqlite:///database.db'
    TEMPLATES_DIR: str = 'templates'
    LOGGING_DIR: str = 'logs'
    LOG_FILE_NAME: str = 'app.log'
    API_LOG_FILE_NAME: str = 'api.log'
    DB_LOG_FILE_NAME: str = 'db.log'
    BASE_URL: str = "https://adsapi.snapchat.com/v1"
    TOKEN_URL: str = "https://accounts.snapchat.com/accounts/oauth2/token"
    AD_ACCOUNT_ID: str = "f7f89c64-00d6-4039-bb86-bb5a63d21fad"
    ORGANIZATION_ID: str = "eefdd199-ae82-4ae8-97c8-1df28149bf7a"
    CLIENT_ID: str = '5ffeb045-fb34-43b0-9b28-0eb528df191a'
    CLIENT_SECRET: str = 'a197ebe6cd3e6cc6e353'
    REFRESH_TOKEN: str = "hCgwKCjE3MDc3NjA4MTQSpQFcvqbaXKH9fx8zGHGSqzuiz0SQNyhY91R3uR3wLjamvcSSUdCm1FQ08zOJvjAr3-Bfqwo974fY9VOMYGhL6fs8y_QgxvxtoxkzPzIEvVfhYRD23-E7RRMUnzM2xmE06NXnt3Km3HVcxtc6-VJU5ldx6cqxWxs79uEl691viCcXuMbc4dxEP-m7ERvyhOr78qHgzN50V6XcsW6XsJCcrfPjOzvN7Xo"