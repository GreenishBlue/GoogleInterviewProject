// Defines access to the search autocomplete api.
class SearchAutocompleteAPI {
    // Get autocomplete options for the current query string.
    // @param @string queryString
    // @param @function callback - Function to execute on completion.
    autoComplete(queryString, callback) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if(xhttp.readyState == 4 && xhttp.status == 200 && xhttp.responseText) {
                // Assume this always sends back valid JSON.
                var results;
                try {
                    results = JSON.parse(this.responseText);
                } catch (e) {
                    results = [];
                }
                callback(results);
            }
        };
        xhttp.open("GET", `/autocomplete?query=${queryString}`, true);
        xhttp.send();
    }
}

// Mock search autocomplete feature.
class MockSearchAutocompleteAPI {
    autoComplete(queryString, callback) {
        callback(["test", "test 2"]);
    }
}

// Controls the search input view.
class SearchInput {
    constructor(searchDropdown, autoCompleteApi) {
        var searchInput = document.getElementById("search_input");
        searchInput.addEventListener("keyup", () => this.onSearchInputChange(), false);

        this._searchDropdown = searchDropdown;
        this._autoCompleteApi = autoCompleteApi;
    }

    onSearchInputChange() {
        var searchInput = document.getElementById("search_input");
        var queryString = searchInput.value;
        console.log("Query string updated: " + queryString);

        // Call autocomplete api. Pass along a function to set results.
        this._autoCompleteApi.autoComplete(queryString, (results) => this._searchDropdown.setResults(results));

        // Hide dropdown if no input.
        this._searchDropdown.setVisible(searchInput.value !== "");
        this._searchDropdown.setMessage("Loading..");
    }
}

// Controls the search dropdown view.
class SearchDropdown {
    constructor() {
        this._searchDropdown = document.getElementById("search_dropdown");
        this._searchDropdown.style = "display: none;";
    }

    // Set the results of the dropdown.
    // @param @[string] results - An array of string results.
    setResults(results) {
        if(!results || !results.length) {
            this.setMessage("No suggestions available");
            return;
        }

        var htmlString = "";
        var url = "./q/title";
        var title = "title";

        results.forEach(result => {
            htmlString += `<li class="list-group-item"><a href="/search?query=${result}">${result}</a></li>`;
        });

        this._searchDropdown.innerHTML = htmlString;
    }

    setMessage(message) {
        this._searchDropdown.innerHTML = `<li class=\"list-group-item\"><b>${message}</b></li>`;
    }

    // Set the dropdown visible.
    // @param @boolean visible
    setVisible(visible) {
        if(visible) {
            this._searchDropdown.style = "";
        }
        else {
            this._searchDropdown.style = "display: none;";
        }
    }
}

// Setup event listeners and stuff here.
function main() {
    console.log("Page loaded!");

    var autoCompleteApi = new SearchAutocompleteAPI();
    var searchDropdown = new SearchDropdown();
    new SearchInput(searchDropdown, autoCompleteApi);
}

// Execute when loaded.
document.addEventListener('DOMContentLoaded', main(), false);