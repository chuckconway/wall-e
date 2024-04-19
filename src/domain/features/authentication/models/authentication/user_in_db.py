from src.domain.features.authentication.models.authentication.user import User


class UserInDB(User):
    hashed_password: str
