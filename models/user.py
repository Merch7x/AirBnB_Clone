"""Creates a user class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Creates a user class instance"""
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
