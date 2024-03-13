# imports
from flask import Flask, render_template, request
from search import Database

# setting up database and app
db = Database("../datasets/edges.txt.gz", "../datasets/titles.txt.gz")
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/solution')
def solution():
    start_page = request.args.get('page').strip()

    try:
        start_id = db.get_id_from_name(start_page)
    except:
        return render_template("bad-page.html", page=start_page)
    
    try:
        path_ids = db.get_path(start_id)
    except:
        return render_template("no-path.html", page=start_page)

    return render_template("solution.html", sites=ids_to_sites_dicts(path_ids), clicks=len(path_ids), start=start_page)


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
        url = "https://en.wikipedia.org/wiki/" + name.replace(" ", "_")
        out_list.append({"name": name, "url": url})
    return out_list


if __name__ == '__main__':
    app.run(debug=True)