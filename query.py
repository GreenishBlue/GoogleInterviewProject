# Author: Cameron Brown
# Date: 18/03/2019
# Purpose: Provides functionality for parsing queries.

from models import Gender, AnimalType

"""
Purpose: Parses queries to find appropriate genders and animal types.
"""
class QueryParser:
    MALE_KEYWORDS = ["boy", "male"]
    FEMALE_KEYWORDS = ["girl", "female"]
    CAT_KEYWORDS = ["cats", "cat"]
    DOG_KEYWORDS = ["dogs", "dog"]
    RABBIT_KEYWORDS = ["rabbits", "rabbit"]

    # Words to remove out of the query.
    EXCLUDED_WORDS = ["and", "or", "all", "with", "colouring", "colour"]

    def __init__(self, query_string):
        self.animal_gender = None
        self.animal_type = None
        self.filtered_query = str(query_string)

        for exclude in self.EXCLUDED_WORDS:
            if exclude in self.filtered_query:
                self.filtered_query = self.filtered_query.replace(exclude, "")

        for pronoun in self.FEMALE_KEYWORDS:
            if pronoun in self.filtered_query:
                self.animal_gender = Gender.Female
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.MALE_KEYWORDS:
            if pronoun in self.filtered_query:
                self.animal_gender = Gender.Male
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.CAT_KEYWORDS:
            if pronoun in self.filtered_query:
                self.animal_type = AnimalType.Cat
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.DOG_KEYWORDS:
            if pronoun in self.filtered_query:
                self.animal_type = AnimalType.Dog
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.RABBIT_KEYWORDS:
            if pronoun in self.filtered_query:
                self.animal_type = AnimalType.Rabbit
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        print(self.filtered_query)