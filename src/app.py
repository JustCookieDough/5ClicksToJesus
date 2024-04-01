"""
# TODO: write description
"""
# imports
from flask import Flask, render_template, request
from search import Database

# setting up database and app
print('building database... (this is going to take a while)')
db = Database("links.txt.gz", "pages.txt.gz")
print('done! setting up flask app...')
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.jinja")


@app.route('/solution')
def solution():
    start_page = request.args.get('page').strip()

    try:
        start_id = db.get_id_from_name(start_page.replace(" ", "_"))
    except:
        return render_template("bad-page.jinja", page=start_page)

    try:
        path_ids = db.get_path(start_id)[:-1]  # removes jesus from end of list
    except:
        return render_template("no-path.jinja", page=start_page)

    return render_template("solution.jinja", sites=ids_to_sites_dicts(path_ids),
                           clicks=len(path_ids), start=start_page)


def ids_to_sites_dicts(ids: list[id]) -> list[dict[str, str]]:
    """
    Converts a list of names into a list of dicts in the shape of:
    {"name": [page_name], "url": [page_url]}
    where page_name is the name passed into the function,
    and page_url is the Wikipedia URL for that page.

    See https://en.wikipedia.org/wiki/Help:URL for more info
    """
    out_list = []
    for id in ids:
        name = db.get_name_from_id(id)
        url = "https://en.wikipedia.org/wiki/" + name
        out_list.append({"name": prettify(name), "url": url})
    return out_list


def prettify(string: str) -> str:
    return string.replace("_", " ")


if __name__ == '__main__':
    app.run(debug=True)

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
