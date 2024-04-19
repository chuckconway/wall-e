import os

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings:

    @staticmethod
    def encryption_key():
        return os.getenv("ENCRYPTION_KEY")

    @staticmethod
    def algorithm():
        return os.getenv("ALGORITHM")

    @staticmethod
    def access_token_expire_minutes():
        return os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

