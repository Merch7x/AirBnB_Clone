"""Creates a city class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Creates an city instance"""

    state_id: str = ""
    name: str = ""
