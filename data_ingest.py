# Author: Cameron Brown
# Date: 14/03/2019
# Purpose: Ingest the .csv data file to the SQL database.

import os
import argparse

from data_format import PetsDataExtractor
from autocomplete import AutoCompleteKeywordGenerator
from db import PetsDatabaseSQLite


# Define the constants for the program. These are DEFAULTS.
DEFAULT_ENABLE_UNSPLASH = False
DEFAULT_ENABLE_GEOCODING = True
DEFAULT_FLAG_FRESH = True # Database reset on run?
DEFAULT_FLAG_DRY_RUN = False
DEFAULT_FLAG_VERBOSE = True

DEFAULT_CSV_PATH = "./pets_raw.csv"
DEFAULT_DB_PATH = "./pets.db"


"""Ingests data into the SQL database."""
class PetsDataIngester:
    """
    Purpose: Sets up the PetsDataIngester.
    Args:
        - listings List of listings (heh) to persist into the database [Listing(), ..]
        - dry_run Is this a dry run/test? bool
        - debug Print debug strings? bool
    """
    def __init__(self, db, listings, dry_run=False, debug=False):
        self.db = db
        self.animal_listings = listings
        self.dry_run = dry_run
        self.debug = debug


    """
    Purpose: Ingest the data into the database.
    """
    def ingest_all(self):
        session = self.db.new_session()

        for listing in self.animal_listings:
            session.add(listing)

        if self.dry_run:
            print("Not persisting data! Dry run mode.")
            
        try:
            session.commit()
            print("Persisted", len(self.animal_listings), "listings to database!")
        except Exception as e:
            session.rollback()
            raise
        finally:
            session.close()


if __name__ == '__main__':
    # Arguments & defaults
    parser = argparse.ArgumentParser()
    parser.add_argument('--geocoding', action='store_true', default=DEFAULT_ENABLE_GEOCODING)
    parser.add_argument('--unsplash', action='store_true', default=DEFAULT_ENABLE_UNSPLASH)
    parser.add_argument('--fresh', action='store_true', default=DEFAULT_FLAG_FRESH)
    parser.add_argument('--csv_in', action='store_true', default=DEFAULT_CSV_PATH)
    parser.add_argument('--out', action='store_true', default=DEFAULT_DB_PATH)
    parser.add_argument('--dry_run', action='store_true', default=DEFAULT_FLAG_DRY_RUN)
    parser.add_argument('-v', action='store_true', default=DEFAULT_FLAG_VERBOSE)

    options = parser.parse_args()
    enable_unsplash = options.unsplash
    enable_geocoding = options.geocoding
    verbose = options.v
    dry_run = options.dry_run
    fresh = options.fresh
    csv_path = options.csv_in
    db_out_path = options.out

    # Connect to the database. Check flags to see if we're in test mode.
    with open(csv_path, "r") as csv_raw:
        data_extractor = PetsDataExtractor(csv_raw, enable_geocoding=enable_geocoding, enable_unsplash=enable_unsplash)
        listings_raw = data_extractor.parse_all()

    listings = data_extractor.to_listings(listings_raw)

    # Establish a connection to the database.
    db = PetsDatabaseSQLite(db_path=db_out_path, fresh=fresh, debug=verbose)

    data_ingester = PetsDataIngester(db, listings, dry_run=dry_run)
    data_ingester.ingest_all()