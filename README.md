# Google Project Challenge - Data Display and Search
Find and view data about pets! 

## Features
* Search through the adoptable pets database
* Autocomplete
* Address geocoding

## Requirements
* Tested on Python 3.7, so let's go with that
* Deps in requirements.txt (see below)
* This was developed on both Windows 10 & Debian 9 Stretch, so presumably any Unix system will be fine
* Network connection if geocoding enabled

### Installing dependencies
`sudo apt-get install python3 python3-pip`
`pip3 install -r requirements.txt`

## Usage
### Running the server (debug mode)
Simply execute the program like so. Uses the Flask debug server by default.

`python3 main.py`

Make sure you execute in the same CWD as the ingest command, otherwise the `pets.db` won't be in the expected location.

### Extracting the data into the database
This will likely not be required if I have included `pets.db` in the repo, however for brevity I have detailed my approach. I've written a series of scripts to actually get the information into a database. Simply execute them as follows:

`python3 data_ingest.py`

This will output the pets database to `pets.db`. Make sure the CWD is the root of the repo.

The `geocoding` flag requires network access and vastly increases processing time, so disable if needed. 

For more help, see:

`python3 data_ingest.py -h`

## Running tests
Each file can be tested simply by running their `test_*.py` counterparts.

## Components
See relevant files for more detailed comments. This project is made of several parts, detailed
below:
* data_*.py - Takes the raw CSV file provided by Google, converts it into 
                   something nicer. Several decisions on filtering/processing are
                   made here. 
                   Will optionally populate the SQL database.
* main.py - Entry point for the Flask-based webapp. This defines the routes and frontend API surface.
* /templates - Contains all Jinja2-based templates
* /static - Contains static assets, most notably CSS and client-side scripts

## Limitations
* Only one breed extracted per animal listing. This was to prevent a many-to-many relationship and a lot of complexity.
* Full autocomplete keyword dictionary is stored in memory - may fail with a large number of keywords.