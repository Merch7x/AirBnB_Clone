"""Creates a review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Creates a review object"""
    place_id: str = ""
    user_id: str = ""
    text: str = ""
