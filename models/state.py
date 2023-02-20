#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'

    name = Column(string(128), nullable=False)
    cities = relationship('City', backref=backref('state', lazy='dynamic'), cascade='all, delete-orphan')

    class FileStorage:
        def __init__(self):
            self.__file_path = 'file.json'
            self.__objects = {}

        @property
        def cities(self):
            return [city for city in self.__objects.values() if
                    city.__class__.__name__ == 'City' and city.state_id == self.id]


