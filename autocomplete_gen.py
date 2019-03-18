# Author: Cameron Brown
# Date: 18/03/2019
# Purpose: Generate a list of keywords for the program.

from models import Listing
from autocomplete import AutoCompleteKeywordGenerator
from db import PetsDatabaseSQLite


db_out_path = "./pets.db"
keywords_path = "./pets_search_keywords.txt"


# Establish a connection to the database.
db = PetsDatabaseSQLite(db_path=db_out_path, fresh=False, debug=False)

listings = db.new_session().query(Listing).all()

print("Generating keywords file")
keyword_gen = AutoCompleteKeywordGenerator(listings)
keyword_gen.generate_all()
keyword_string = keyword_gen.to_string()

with open(keywords_path, "w") as keywords_file:
    keywords_file.write(keyword_string)
    keywords_file.close()