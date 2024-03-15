
import gzip


class Node():
    """
    # TODO: figure this jawn out
    """
    def __init__(self) -> None:
        pass


# TODO: all of this needs to be rewritten for the new db's from wikidump
class Database():
    """
    # TODO: write a docstring and also finish this lmao
    """
    def __init__(self, edge_file_path, title_file_path) -> None:
        self._titles = self._load_titles(title_file_path)
        self._pages = self._load_edges(edge_file_path)


    def _load_titles(self, path: str) -> dict[int, str]: # slow and bad but works
        """
        loads the titles into a dict: {id: name}

        # TODO: write better docstring
        # TODO: rewrite for wikidump
        """
        out_dict = {}
        with gzip.open(path, "r") as file:
            for line in file:
                data = str(line, 'utf-8').strip().split(" ")
                out_dict[int(data[0])] = str(data[1]).replace("\\'", "'").replace('\\"','"').replace('\\\\', '\\')
        return out_dict        


    def _load_edges(self, path: str) -> list[Node]:
        # TODO: write this
        pass


    def get_name_from_id(self, id: int) -> str:
        """
        Returns a page's name when given its id
        """
        if id in self._titles:
            return self._titles[id]
        raise KeyError("name not in titles database")


    def get_id_from_name(self, name: str) -> int:
        """
        Returns a page's id when given its name
        """
        for key in self._titles:
            if self._titles[key] == name:
                return key
        raise KeyError("id not in titles database")


    def get_path(self, id: int) -> list[int]:
        # TODO: implement this (lmao easier said than done)

        # everything below was added by scott to make it easier to test the front-end
        # delete it when you actually write this
        return [id, 1095706]  # just a base case