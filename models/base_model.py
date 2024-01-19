#!/usr/bin/env python3
"""Define a baseclass to be used by a superclass by other classes"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """Creates an instance of base Model"""

    def __init__(self, *args, **kwargs):
        """Instanciates the object with dict from kwargs if not empty
        else define values

        Args:
            *args(any): Not used
            **kwargs(dict): key value pairs
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    formatted_value = self.format_value(key, value)
                    # makes the code more robust
                    setattr(self, key, formatted_value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def format_value(self, key, value):
        """formats the value depending on expected type
        before setting them if kwargs is not none
        """
        if key in ['created_at', 'updated_at']:
            # dateutils for older python versions
            return datetime.fromisoformat(value)
        elif key == 'id':
            return str(value)  # not neccessary just a precaution
        else:
            return value

    def __str__(self):
        """Prints a user friendly output"""
        return f"{[self.__class__.__name__]} {(self.id)} {self.__dict__}"

    def save(self):
        """Updates the instance variable updated_at
        with the current datetime and saves s json string
        to file storage
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of
        __dict__ instance
        """
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['updated_at'] = self.updated_at.isoformat()
        return my_dict
