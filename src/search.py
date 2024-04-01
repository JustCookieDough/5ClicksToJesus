"""
# TODO: write description
"""
from __future__ import annotations
import gzip
from typing import Any
# import csv
# import os


class _Node:
    """A node in a graph used to represent a Wikipedia page.

    Instance Attributes:
        - item: The data stored in this node.
        - out_neighbors: Nodes that this node has an edge to.
        - in_neighbors: Nodes that have an edge to this node.
        - next_node_to_target: the next Node in the shortest path to the target.
        -1 for the target

    Representation Invariants:
        - self not in self.out_neighbors
        - self.id_num >= 0
        - self.next_node_to_target != self.id_num
        - self.next_node_to_target in out_neighbors
    """
    id_num: int
    out_neighbors: list[_Node]
    in_neighbors: list[_Node]
    next_node_to_target: _Node

    def __init__(self, id_num: int, out_neighbors: list[_Node],
                 in_neighbors: list[_Node]) -> None:
        """Initialize a new node with the given item and neighbours."""
        self.id_num = id_num
        self.out_neighbors = out_neighbors
        self.in_neighbors = in_neighbors
        # self.next_node_to_target = None


class Graph:
    """A graph used to represent the out_neighbors between Wikipedia pages.

    Representation Invariants:
        - all(id_num == self._nodes[id_num].id_num for id_num in self._nodes)
    """
    # Private Instance Attributes:
    #     - _nodes:
    #         A collection of the nodes contained in this graph.
    #         Maps Wikipedia pages to _Node object.
    _nodes: dict[Any, _Node]
    target_id: int

    def __init__(self) -> None:
        """Initialize an empty graph (no nodes or edges)."""
        self._nodes = {}

    def add_node(self, id_num: Any) -> None:
        """Add a node with the given id_num to this graph.

        The new node is not adjacent to any other nodes.

        Preconditions:
            - id_num not in self._nodes
        """
        if id_num not in self._nodes:
            self._nodes[id_num] = _Node(id_num, [], [])

    def add_edge(self, id1: Any, id2: Any) -> None:
        """Add an edge from the node with id1 to the node with id2 in this
        graph.

        Raise a ValueError if item1 or item2 do not appear as nodes in this graph.

        Preconditions:
            - id1 != id2
        """
        if id1 in self._nodes and id2 in self._nodes:
            v1 = self._nodes[id1]
            v2 = self._nodes[id2]

            v1.out_neighbors.append(v2)
            v2.in_neighbors.append(v1)
        else:
            raise ValueError

    def compute_paths(self, target_id: int) -> None:
        """
        Computes the paths to the target for all nodes connected to the target. This should be
        called after all the edges have been added to a graph and before calling get_path.

        Raise a ValueError if target_id is not in this dataset.
        """
        if target_id not in self._nodes:
            raise ValueError
        self._nodes[target_id].next_node_to_target = -1
        self.target_id = target_id
        q = [target_id]
        while len(q) != 0:
            curr = q.pop(0)
            for node in self._nodes[curr].in_neighbors:
                if node.next_node_to_target is None:
                    node.next_node_to_target = self._nodes[curr]
                    q.append(node.id_num)

    def get_path(self, id_num: int) -> list[int]:
        """Return a list of the id_num's of the shortest path to the target. Returns an empty list if
        this id_num is not connected to the target.

        Raise a ValueError if id_num is not in this dataset.
        """
        path = []
        if id_num not in self._nodes:
            raise ValueError
        curr = self._nodes[id_num]
        if curr.next_node_to_target is None:
            return []
        path.append(curr.id_num)
        while curr.id_num != self.target_id:
            curr = curr.next_node_to_target
            path.append(curr.id_num)
        return path


class Database:
    """
    A Database with a corresponding Graph representing all Wikipedia pages as vertices and
    all connecting hyperlinks as edges. Has functionality to correlate titles to pages IDs.

    Instance Attributes:
        - _titles: dict of page id number to title
        - _graph = directed graph representing the pages and links between them
    """
    _titles: set
    _graph: Graph

    def __init__(self, edge_file_path: str, title_file_path: str) -> None:
        self._titles = self._load_titles(title_file_path)
        self._graph = self._load_graph(edge_file_path)
        self._graph.compute_paths(
            1095706)  # 60047 is the ID for page "Jesus" in the links.txt data.
        # TODO: verify above input for new data

    def _load_titles(self, path: str) -> dict[int, str]:  # slow and bad but works
        """
        Using the data given from path, loads the Wikipedia page titles into a dict relating
        {id: name}

        # TODO: rewrite for wikidump
        ^^^ Removed the previous to-do since it was redundant. I think it's okay if the wikidump is the one sent on
        insta with google drive link, If im not mistaken, that is also data separated with spaces and should work for
        this, please confirm.
        """
        out_dict = {}
        with gzip.open(path, "r") as file:
            for line in file:
                data = str(line, 'utf-8').strip().split(" ")
                out_dict[int(data[0])] = str(data[1]).replace("\\'", "'").replace('\\"',
                                                                                  '"').replace(
                    '\\\\', '\\')
        return out_dict

    def _load_graph(self, path: str) -> Graph:
        """
        Loads the graph, establishing all connected pages as vertices and all connected links as edges from the given
        edges file. Note: if there is a page with no neighbours, it will not be present in the edges file and hence
        will not be contained in this graph. This is intentional for memory and efficiency purposes.
        """
        graph = Graph()
        with gzip.open(path, 'r') as file:
            for line in file:
                edges = str(line, "utf-8").strip().split(" ")
                graph.add_node(int(edges[0]))
                graph.add_node(int(edges[1]))
                graph.add_edge(int(edges[0]), int(edges[1]))
        return graph

    def get_name_from_id(self, id_num: int) -> str:
        """
        Returns a page's name when given its id_num
        """
        if id_num in self._titles:
            return self._titles[id_num]
        raise KeyError("name not in titles database")

    def get_id_from_name(self, name: str) -> int:
        """
        Returns a page's id when given its name
        """
        for key in self._titles:
            if self._titles[key] == name:
                return key
        raise KeyError("id not in titles database")


if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['gzip'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
