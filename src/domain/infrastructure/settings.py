import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env.local')
load_dotenv(dotenv_path)


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

    @staticmethod
    def jwt_expire_weeks() -> int:
        weeks = os.getenv("JWT_TOKEN_EXPIRE_WEEKS")
        return int(weeks)
