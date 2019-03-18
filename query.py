# Author: Cameron Brown
# Date: 18/03/2019
# Purpose: Provides functionality for parsing queries.

from models import Gender, AnimalType

"""
Purpose: Parses queries to find appropriate genders and animal types.
"""
class QueryParser:
    MALE_PRONOUNS = ["boy", "male"]
    FEMALE_PRONOUNS = ["girl", "female"]
    CAT_PRONOUNS = ["cats", "cat"]
    DOG_PRONOUNS = ["dogs", "dog"]
    RABBIT_PRONOUNS = ["rabbits", "rabbit"]

    # Words to remove out of the query.
    EXCLUDES = ["and", "or", "all", "with", "colouring", "colour"]

    def __init__(self, query_string):
        self.animal_gender = None
        self.animal_type = None
        self.filtered_query = str(query_string)

        for exclude in self.EXCLUDES:
            if exclude in self.filtered_query:
                self.filtered_query = self.filtered_query.replace(exclude, "")

        for pronoun in self.FEMALE_PRONOUNS:
            if pronoun in self.filtered_query:
                self.animal_gender = Gender.Female
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.MALE_PRONOUNS:
            if pronoun in self.filtered_query:
                self.animal_gender = Gender.Male
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.CAT_PRONOUNS:
            if pronoun in self.filtered_query:
                self.animal_type = AnimalType.Cat
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.DOG_PRONOUNS:
            if pronoun in self.filtered_query:
                self.animal_type = AnimalType.Dog
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        for pronoun in self.RABBIT_PRONOUNS:
            if pronoun in self.filtered_query:
                self.animal_type = AnimalType.Rabbit
                self.filtered_query = self.filtered_query.replace(pronoun, "")

        print(self.filtered_query)