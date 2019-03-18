# Author: Cameron Brown
# Date: 14/03/2019
# Purpose: Represents the database models.

import os, sys
import enum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import Enum
from sqlalchemy import PickleType
from sqlalchemy import Sequence

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Animal enumeration.
class AnimalType(enum.Enum):
    Unknown = 0
    Cat = 1
    Dog = 2
    Rabbit = 3


# Gender enumeration.
class Gender(enum.Enum):
    Unknown = 0
    Male = 1
    Female = 2


# Listing db model.
class Listing(Base):
    __tablename__ = 'listing'
    id = Column(Integer(), 
        Sequence('article_aid_seq', start=10000, increment=1), primary_key=True)
    animal_name = Column(String(256))
    animal_breed = Column(String(256))
    animal_sterilised = Column(Boolean())
    animal_gender = Column(Enum(Gender))
    
    animal_type = Column(Enum(AnimalType), default=AnimalType.Unknown) # cat, dog, rabbit, etc..
    photo_url = Column(String(256))

    animal_colours = Column(String(256))

    address_lat = Column(Float())
    address_lng = Column(Float())
    address_city = Column(String(256))

    def has_photo_url(self):
        return self.photo_url is not None

    def get_photo_url(self):
        return "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb"

    def get_title(self):
        if not self.animal_name:
            return "Hi!"
        return "Meet " + self.animal_name + "!"

    def get_colouring(self):
        if self.animal_colours is None or self.animal_colours == "":
            return ""
        return " with " + self.animal_colours.lower() + " colouring"

    def get_breed(self):
        if self.animal_breed is None:
            return ""
        return self.animal_breed.lower()

    def get_city(self):
        if self.address_city is None:
            return ""
        return ", from " + self.address_city

    def get_gender(self):
        if self.animal_gender is Gender.Male:
            return " male "
        elif self.animal_gender is Gender.Female:
            return " female "
        else:
            return " "

    def get_sterilised(self):
        if not self.animal_sterilised:
            return " "
        elif self.animal_gender is Gender.Male:
            return " (neutured) "
        elif self.animal_gender is Gender.Female:
            return " (spayed) "
        else:
            return " "

    def get_description(self):
        return "I'm a" + self.get_sterilised() + self.get_gender() + self.get_breed() + self.get_colouring() + self.get_city() + "."

    def has_map_url(self):
        return self.address_lat is not None and self.address_lng is not None

    def get_map_url(self):
        return "https://maps.google.com/?q=" + str(self.address_lat) + "," + str(self.address_lng)