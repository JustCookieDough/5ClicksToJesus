"""
Description: Use a graph to represent the links between wikipedia pages to in order to calculate
the shortest path to Jesus from any given page.
Date: 2024-04-01
Authors: Maxwell Antao Zhang, Yin Ming Chan, Alex Lewis, Scott Angelides
"""
# imports
from flask import Flask, render_template, request
from search import Database


class App:
    """The program

    Instance Attributes:
        - db: the database of wikipedia
        - app: interactive app
    """
    db: Database
    app: Flask

    def __init__(self, edge_file_path: str, title_file_path: str) -> None:
        """"""
        # setting up database and app
        print('building database... (this is going to take a while)')
        self.db = Database(edge_file_path, title_file_path)
        print('done! setting up flask app...')
        app = Flask(__name__)

        @app.route('/')
        def index() -> str:
            return render_template("index.jinja")

        @app.route('/solution')
        def solution() -> str:
            start_page = request.args.get('page').strip()

            try:
                start_id = self.db.get_id_from_name(start_page.replace(" ", "_"))
            except:
                return render_template("bad-page.jinja", page=start_page)

            try:
                path_ids = self.db.get_path(start_id)[:-1]  # removes jesus from end of list
            except:
                return render_template("no-path.jinja", page=start_page)

            return render_template("solution.jinja", sites=self.ids_to_sites_dicts(path_ids),
                                   clicks=len(path_ids), start=start_page)

        self.app = app

    def ids_to_sites_dicts(self, ids: list[id]) -> list[dict[str, str]]:
        """
        Converts a list of names into a list of dicts in the shape of:
        {"name": [page_name], "url": [page_url]}
        where page_name is the name passed into the function,
        and page_url is the Wikipedia URL for that page.

        See https://en.wikipedia.org/wiki/Help:URL for more info
        """
        out_list = []
        for id_num in ids:
            name = self.db.get_name_from_id(id_num)
            url = "https://en.wikipedia.org/wiki/" + name
            out_list.append({"name": self.prettify(name), "url": url})
        return out_list

    def prettify(self, string: str) -> str:
        """Formats strings with spaces instead of underscores."""
        return string.replace("_", " ")

    def run(self) -> None:
        """Runs the app."""
        self.app.run(debug=True)


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['flask', 'search'],  # the names (strs) of imported modules
        'allowed-io': ['App.__init__'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
