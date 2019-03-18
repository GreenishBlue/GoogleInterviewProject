# Author: Cameron Brown
# Date: 16/03/2019
# Purpose: Provides autocomplete for the program.

"""
Purpose: Generates a list of query suggestions, provided a prefix and (a set of 
         known keywords AoT).
"""
class AutoCompleter:
    MAX_SUGGEST_COUNT = 3 # trie only

    """
    Purpose: Sets up the AutoCompleter.
    """
    def __init__(self, keywords):
        # We want to generate a trie based on these keywords.
        self.keywords = keywords


    """
    Purpose: Brute-force implementation of keyword search - O(n).
    """
    def linear_keyword_search(self, prefix):
        suggestions = []
        for keyword in self.keywords:
            if keyword.startswith(prefix):
                suggestions.append(keyword)
        return suggestions


    """
    Purpose: Return several query suggestions for a given prefix.
    Args:
        - prefix The query prefix : string
    Returns:
        - Array of suggestions : [string]
    """
    def auto_complete(self, prefix):
        prefix = prefix.lower()
        prefix_words = prefix.split()
        if len(prefix_words) > 1:
            curr_word = prefix_words[-1]

            suffix_suggestions = self.linear_keyword_search(curr_word)
            suggestions = []
            # Original query minus current word.
            original_query = prefix.rsplit(' ', 1)[0]

            for suggestion in suffix_suggestions:
                suggestions.append(original_query + " " + suggestion)

            return suggestions[:3]
        else:
            return self.linear_keyword_search(prefix)[:3]

"""
Purpose: Generate a list of query keywords from raw csv.
"""
class AutoCompleteKeywordGenerator:
    DEFAULT_KEYWORDS = ["dog", "cat", "rabbit", "male", "female", "boy", "girl"]

    def __init__(self, listings):
        self.keywords = self.DEFAULT_KEYWORDS
        self.listings = listings
    

    def to_string(self):
        my_string = ""
        for keyword in self.keywords:
            my_string += (keyword.lower() + "\n")
        return my_string


    def generate_all(self):
        keywords_dict = {}

        for listing in self.listings:
            if listing.animal_name is None:
                pass
            elif listing.animal_name not in keywords_dict:
                keywords_dict[listing.animal_name] = True

            if listing.animal_breed is None:
                pass
            elif listing.animal_breed not in keywords_dict:
                keywords_dict[listing.animal_breed] = True
            
            if not isinstance(listing.animal_colours, list):
                continue
            for colour in listing.animal_colours:
                if colour not in keywords_dict:
                    keywords_dict[colour.lower()] = True
                self.keywords.append(colour.lower())
        
        self.keywords = list(keywords_dict.keys())