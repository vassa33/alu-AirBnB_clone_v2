#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel


class City(BaseModel):
    """ The city class, contains state ID and name """

    __tablename__ = 'cities'
    state_id = Column(string(60), ForeignKey("states.id"), nullable=False)
    name = Column(string(128), nullable=False)
    places = relationship("Place", backref="cities")
