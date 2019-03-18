# Author: Cameron Brown
# Date: 14/03/2019
# Purpose: Runs the web server.

from flask import *
app = Flask(__name__)

from db import PetsDatabaseSQLite
from models import *
from autocomplete import AutoCompleter
from query import QueryParser


TITLE = "Adopt-A-Pet"
DB_FILENAME = "pets.db"
DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), DB_FILENAME)
KEYWORDS_FILENAME = "pets_search_keywords.txt"
KEYWORDS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), KEYWORDS_FILENAME)


# Avoiding any kind of dependency injection for this simple example.
auto_completer = None


@app.route("/")
def route_index():
    return render_template("index.html", title=TITLE, page_title=TITLE)


@app.route("/autocomplete")
def route_autocomplete():
    query = request.args.get('query')
    print(query)
    return jsonify(auto_completer.auto_complete(query))


@app.route("/search")
def route_query():
    db = PetsDatabaseSQLite(DB_PATH)

    query = request.args.get('query')
    page_number = request.args.get('page') or 1
    page_number = int(page_number)
    page_max = 1

    if not query:
        return redirect("/")

    session = db.new_session()
    parser = QueryParser(query)
    listings = session.query(Listing) \
        .filter(Listing.animal_breed.like("%" + parser.filtered_query + "%") |
                Listing.animal_colours.like("%" + parser.filtered_query.strip() + "%") |
                Listing.animal_name.like("%" + parser.filtered_query + "%"))
    
    if parser.animal_type:
        listings = listings.filter(Listing.animal_type == parser.animal_type)
    
    if parser.animal_gender:
        listings = listings.filter(Listing.animal_gender == parser.animal_gender)

    return render_template("search.html", title=query + " - Search", page_title=TITLE, search_data=query, 
        page_number=page_number, query=query, page_max=page_max, listings=listings, listings_len=50)


if __name__ == '__main__':
    # Load keywords and setup the autocompleter.
    keywords = []
    with open(KEYWORDS_PATH, "r") as keywords_file:
        lines = keywords_file.readlines()
        for line in lines:
            keywords.append(line.replace('\n', ''))
    keywords.sort()
    auto_completer = AutoCompleter(keywords)
    
    app.run(debug=True, host='0.0.0.0', port=8080)