# Author: Cameron Brown
# Date: 14/03/2019
# Purpose: Format the .csv file provided by Google.

# Overview:
# 1. Open the file.
# 2. Parse the data into the appropriate structure.
# 3. Convert the structure to app-specific one.
# 4. Export interface allowing other scripts to use this one.

import re
import os
import csv
import requests
from unsplash.api import Api
from unsplash.auth import Auth
import geocoder
from models import *


"""Represents a single row of the pets_raw csv"""
class PetRaw:
    def __init__(self, id, name, animal_type, address, gender, breeds, colours, 
                 sterilised=False, deceased=False):
        self.id = id
        self.name = name
        self.animal_type = animal_type
        self.address = address
        self.gender = gender
        self.breeds = breeds
        self.colours = colours
        self.sterilised = sterilised
        self.deceased = deceased


"""Extracts and cleans up the raw dataset."""
class PetsDataExtractor:
    """Setup the data formatter."""
    def __init__(self, csv_raw, enable_geocoding=False, debug=False):
        self.raw = csv_raw
        self.pets = []
        self.debug = debug
        self.enable_geocoding = enable_geocoding


    """
    Purpose: Parse the raw .csv data.
    Returns: 
        - Array of PetRaw objects [PetRaw()] 
    """
    def parse_all(self):
        reader = csv.DictReader(self.raw)
        for row in reader:
            pet = self.parse(row)
            if pet:
                self.pets.append(pet)
            if self.debug:
                print(vars(pet))
        return self.pets


    """
    Purpose: Returns a provided value or a NoneType.
    Args:
        - type Raw value : string
    Returns: 
        - string or NoneType
    """
    def parse_value(self, value):
        if not value:
            return None
        return value


    """
    Purpose: Parse the animal_type column.
    Args:
        - type_string Raw animal type : string
    Returns: Tuple containing the extracted animal type, and a deceased bool:
            (string : animal_type, boolean : deceased)
    """
    def parse_animal_type(self, type_string):
        # We'll try not to assume the worst.
        deceased = False

        # Nothing we can do here.
        if not type_string:
            return (AnimalType.Unknown, False)

        if "Dead" in type_string:
            # Check if animal is dead and trim string.
            # Again, that's cold..
            deceased = True
            type_string = type_string.replace("Dead ", "")

        # Convert to hard value.
        if "Dog" in type_string:
            return (AnimalType.Dog, deceased)
        elif "Cat" in type_string:
            return (AnimalType.Cat, deceased)
        elif "Rabbit" in type_string:
            return (AnimalType.Rabbit, deceased)
        
        return (AnimalType.Unknown, False)


    """
    Purpose: Parse the Animal_Breed column.
    Args:
        - breeds_string Raw breeds string : string
    Returns: 
    -    Array of breed strings : [string]
    """
    def parse_breeds(self, breeds_string):
        # Split breeds into a list.
        if breeds_string:
            return re.split('/|\|,| / | \ ', breeds_string)
        else:
            return []


    """
    Purpose: Parse the Animal_Gender column.
    Args:
        - gender_string Raw gender string : string
    Returns: 
        - Gender enum and sterilised bool : (Gender, boolean)
    """
    def parse_gender(self, gender_string):
        gender = Gender.Unknown
        sterilised = False

        # Check sterlilisation status. God that sounds cold.
        if "Intact" in gender_string:
            gender_string = gender_string.replace("Intact ", "")
        elif "Unaltered" in gender_string:
            gender_string = gender_string.replace("Unaltered ", "")
        elif "Spayed" in gender_string:
            sterilised = True
            gender_string = gender_string.replace("Spayed ", "")
        elif "Neutered" in gender_string:
            sterilised = True
            gender_string = gender_string.replace("Neutered ", "")

        # Check actual gender.
        if "Male" in gender_string:
            gender = Gender.Male
        elif "Female" in gender_string:
            gender = Gender.Female

        return (gender, sterilised)


    """
    Purpose: Parse the colours string.
    Args:
        - colours_string Raw colour string : string
    Returns: 
        - Array of colour strings : [string]
    """
    def parse_colours(self, colours_string):
        if not colours_string or colours_string == "Unknown":
            return []
        else:
            return re.split('/|\|,| / | \ | ', colours_string)


    """
    Purpose: Parse one row of data and return a PetRaw()
             Handling Edge Cases: oh boy this is gonna get messy.
    Assumptions:
        - No missing keys from csv file.
    Args:
        - row: Single CSV row.
    Returns: Parsed PetRow() object."""
    def parse(self, row):
        id = row["Animal_ID"] # No missing keys, so assume it is here.
        name = self.parse_value(row["Animal_Name"])
        (animal_type, deceased) = self.parse_animal_type(row["animal_type"])
        address = self.parse_value(row["Address"])
        breeds = self.parse_breeds(row["Animal_Breed"])
        (gender, sterilised) = self.parse_gender(row["Animal_Gender"])
        colours = self.parse_colours(row["Animal_Color"])

        return PetRaw(id, name, animal_type, address, gender, breeds, colours, 
            sterilised=sterilised, deceased=deceased)

    """
    Purpose: Extract listings from each row.
    Assumptions:
        - Each listing has a unique identifier.
        - Addresses have been geocoded into a lat/lng formatting.
    Returns:
        - List of Listing() objects [Listing(), ..]
    """
    def to_listings(self, rows):
        # Each one is unique, so we don't need hashtable semantics.
        listings = []

        for row in rows:
            listing = Listing()
            # listing.id = row.id # turns out not unique.. hmm
            listing.animal_name = row.name
            listing.animal_type = row.animal_type
            listing.animal_breed = "/".join(row.breeds)
            listing.animal_sterilised = row.sterilised
            listing.animal_gender = row.gender
            listing.animal_colours = "/".join(row.colours)

            if self.enable_geocoding and row.address is not None:
                address = row.address
                print("Geocoding lookup for ", address)
                geo = geocoder.osm(address)
                if geo is not None and geo.latlng is not None:
                    (lat, lng) = geo.latlng
                    listing.address_lat = lat
                    listing.address_lng = lng
                    listing.address_city = geo.city

            listings.append(listing)
            if self.debug:
                print("Extracted listing!")
        
        return listings