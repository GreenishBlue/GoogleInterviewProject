# Author: Cameron Brown
# Date: 16/03/2019
# Purpose: Manages the database connection.

from models import Base, Listing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


"""Manages a generic pets database."""
class PetsDatabase:
    def __init__(self, engine, fresh, debug):
        self.engine = engine
        if fresh:
            print("Resetting database! Dropped all tables.")
            Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        Listing.metadata.create_all(self.engine)
        self.sessionmaker = sessionmaker(bind=self.engine)


    """
    Purpose: Create new SQAlchemy session.
    Returns:
        - The session.
    """
    def new_session(self):
        return self.sessionmaker()


"""Manages an SQL-lite PetsDatabase."""
class PetsDatabaseSQLite(PetsDatabase):
    def __init__(self, db_path, fresh=False, debug=False):
        print("Connecting to database (SQLite engine)")
        self.engine = create_engine("sqlite:///" + db_path)
        super().__init__(self.engine, fresh, debug)


"""Manages a MySQL PetsDatabase."""
class PetsDatabaseMySQL(PetsDatabase):
    def __init__(self):
        raise NotImplementedError