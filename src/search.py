from __future__ import annotations
import gzip
from typing import Any
import csv


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
        - self.id >= 0
        - self.next_node_to_target != self.id`
        - self.next_node_to_target in out_neighbors
    """
    id: int
    out_neighbors: set[_Node]
    in_neighbors: set[_Node]
    next_node_to_target: _Node

    def __init__(self, id: int, out_neighbors: set[_Node], in_neighbors: set[_Node]) -> None:
        """Initialize a new node with the given item and neighbours."""
        self.id = id
        self.out_neighbors = out_neighbors
        self.in_neighbors = in_neighbors
        self.next_node_to_target = None


class Graph:
    """A graph used to represent the out_neighbors between Wikipedia pages.

    Representation Invariants:
        - all(id == self._nodes[id].id for id in self._nodes)
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

    def add_node(self, id: Any) -> None:
        """Add a node with the given id to this graph.

        The new node is not adjacent to any other nodes.

        Preconditions:
            - id not in self._nodes
        """
        if id not in self._nodes:
            self._nodes[id] = _Node(id, set(), set())

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

            v1.out_neighbors.add(v2)
            v2.in_neighbors.add(v1)
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
                    q.append(node.id)

    def get_path(self, id: int) -> list[int]:
        """Return a list of the id's of the shortest path to the target. Returns an empty list if
        this id is not connected to the target.

        Raise a ValueError if id is not in this dataset.
        """
        path = []
        if id not in self._nodes:
            raise ValueError
        curr = self._nodes[id]
        if curr.next_node_to_target is None:
            return []
        path.append(curr.id)
        while curr.id != self.target_id:
            curr = curr.next_node_to_target
            path.append(curr.id)
        return path


# TODO: all of this needs to be rewritten for the new db's from wikidump
class Database:
    """
    # TODO: write a docstring and also finish this lmao
    """

    def __init__(self, edge_file_path, title_file_path) -> None:
        self._titles = self._load_titles(title_file_path)
        self._graph = self._load_graph(edge_file_path)
        self._graph.compute_paths()

    def _load_titles(self, path: str) -> dict[int, str]:  # slow and bad but works
        """
        loads the titles into a dict: {id: name}

        # TODO: write better docstring
        # TODO: rewrite for wikidump
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
        Load the graph from the edges file.

        If there is a page with no neighbors it will not be in the edges file and hence won't be
        read into the graph. Do we want to change this?
        
        nah should be fine. we can be smarter about it for memory purposes but it wont change 
        how the function runs
        """
        graph = Graph()
        with gzip.open(path, 'r') as file:
            i = 0
            for line in file:
                print(str(round(i/6398388.68, 2)) + "%")
                i += 1

                edges = str(line, "utf-8").strip().split(" ")
                graph.add_node(edges[0])
                graph.add_node(edges[1])
                graph.add_edge(edges[0], edges[1])
        return graph

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
