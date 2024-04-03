"""
Description: Use a graph to represent the links between wikipedia pages to in order to calculate
the shortest path to Jesus from any given page.
Date: 2024-04-01
Authors: Maxwell Antao Zhang, Yin Ming Chan, Alex Lewis, Scott Angelides

A quick note on the style for the below file:
Per the Flask style guide, a Flask app is to be created at module level. As such, the database and webserver (flask
app) initialization will be taking place at the module level. We are aware this violates the typical style
recommendations for a traditional python file, however this is how this library was meant to be used and as such we
followed the established Flask style conventions.

The two helper functions, "prettify" and "ids_to_sites_dicts", are small and not associated with a given class, and
therefore belong at module level.
"""

# imports
import os
from flask import Flask, render_template, request
from search import Database
from tests import run_tests

########################################################################################################################
# getting user input
########################################################################################################################


# intro text :D
os.system('cls' if os.name == 'nt' else 'clear')  # clears the terminal
print('    ______ ______ ___       __')
print('   / ____// ____/|__ \\     / /')
print('  /___ \\ / /     __/ /__  / / ')
print(' ____/ // /___  / __// /_/ /  ')
print('/_____/ \\____/ /____/\\____/   ')
print('\n5 Clicks To Jesus: CSC111 Project 2')
print('by scott, alex, max, and ming!\n\n')

# getting user input on save state use (mostly a TA thing, would be deleted in hypothetical prod build)
selection = ""
while selection not in ("1", "2", "3", "4", "5"):
    if selection != "":
        print("please select 1, 2, 3, 4, or 5\n")

    print('select a dataset mode to build in (build times are estimates):')
    print(' (1) sample dataset (distance 2 or less from jesus) (10s) ')
    print(' (2) current dataset, build from save state (15s)')
    print(' (3) 2010 dataset, full precompute (15min)')
    print(' (4) current dataset, full precompute (>1hr)')
    print(' (5) pyta testing \n')
    selection = input("which mode? ")

selection = int(selection)

########################################################################################################################
# database + webserver setup
########################################################################################################################

# building database
if selection == 1:
    print("\ndatabase version: sample of current (March 1, 2024)\nbuilding database...")
    db = Database("../datasets/current/sample.txt.gz", "../datasets/current/pages.txt.gz", True)
elif selection == 2:
    print("\ndatabase version: current (March 1, 2024)\nbuilding database from save state...")
    db = Database("../datasets/current/saved.txt.gz", "../datasets/current/pages.txt.gz", True)
elif selection == 3:
    print('\ndatabase version: March 12, 2010\nbuilding database...')
    db = Database("../datasets/2010/links.txt.gz", "../datasets/2010/pages.txt.gz")
elif selection == 4:
    print('\ndatabase version: current (March 1, 2024)\nbuilding database...')
    db = Database("../datasets/2010/links.txt.gz", "../datasets/2010/pages.txt.gz")
elif selection == 5:
    print("running tests!")
    run_tests()
    print("tests ran! halting execution! bye! :D")
    exit()

# building the flask app
print('done! setting up flask app...')
app = Flask(__name__)


########################################################################################################################
# webserver endpoints
########################################################################################################################


@app.route('/')
def index() -> str:
    """Renders the index page, returns the rendered DOM as a string."""
    return render_template("index.jinja")


@app.route('/solution')
def solution() -> str:
    """
    Renders the solution page by parsing the requests arguments and querying the database.

    Returns the rendered DOM as a string.
    """
    start_page = request.args.get('page').strip()  # parse request arguments and format for db use

    try:
        start = db.get_id_from_name(start_page.replace(" ", "_"))
    except KeyError:
        return render_template("bad-page.jinja", page=start_page)  # page not in titles db

    try:
        path = db.get_path(start)
    except ValueError:
        return render_template("not-in-graph.jinja",
                               page=start_page)  # page not in graph, but in title (only samples)

    if not path:
        return render_template("no-path.jinja", page=start_page)  # no path found

    if start == 1095706:
        return render_template("solution.jinja", sites=[],
                               clicks=0, start=start_page)
    else:
        return render_template("solution.jinja", sites=ids_to_sites_dicts(path),
                               clicks=len(path), start=start_page)  # normal page (path found!)


########################################################################################################################
# helper functions
########################################################################################################################


def ids_to_sites_dicts(ids: list[int]) -> list[dict[str, str]]:
    """
    Converts a list of names into a list of dicts in the shape of:
    {"name": [page_name], "url": [page_url]}
    where page_name is the name passed into the function,
    and page_url is the Wikipedia URL for that page.

    See https://en.wikipedia.org/wiki/Help:URL for more info
    """
    out_list = []
    for id_num in ids:
        name = db.get_name_from_id(id_num)
        url = "https://en.wikipedia.org/wiki/" + name
        out_list.append({"name": prettify(name), "url": url})
    return out_list


def prettify(string: str) -> str:
    """
    Prettifies strings by replacing underscores with spaces
    """
    return string.replace("_", " ")


########################################################################################################################
# running the app
########################################################################################################################


app.run(port=5678)
