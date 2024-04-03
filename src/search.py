"""
Description: Use a graph to represent the links between wikipedia pages to in order to calculate
the shortest path to Jesus from any given page.
Date: 2024-04-01
Authors: Maxwell Antao Zhang, Yin Ming Chan, Alex Lewis, Scott Angelides
"""
from __future__ import annotations
import gzip
from typing import Any, Optional
from io import FileIO


class _Node:
    """A node in a graph used to represent a Wikipedia page.

    Instance Attributes:
        - item: The data stored in this node.
        - out_neighbors: Nodes that this node has an edge to.
        - in_neighbors: Nodes that have an edge to this node.
        - next_node_to_target: the next Node in the shortest path to the target. self for target.

    Representation Invariants:
        - self not in self.out_neighbors
        - self.id_num >= 0
        - self.next_node_to_target != self.id_num
        - self.next_node_to_target in out_neighbors
    """
    id_num: int
    out_neighbors: list[_Node]
    in_neighbors: list[_Node]
    next_node_to_target: Optional[_Node]

    def __init__(self, id_num: int, out_neighbors: list[_Node],
                 in_neighbors: list[_Node], next_node_to_target: _Node = None) -> None:
        """Initialize a new node with the given item and neighbours."""
        self.id_num = id_num
        self.out_neighbors = out_neighbors
        self.in_neighbors = in_neighbors
        self.next_node_to_target = next_node_to_target


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
        self._nodes[target_id].next_node_to_target = self._nodes[target_id]  # this is stupid, but it works, so
        self.target_id = target_id                                           # therefore it is not stupid :D
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

    def add_node_with_path(self, id_num: int, next_node_id: int) -> None:
        """
        Adds node with id "id_num" and next_node_in_path "next_node_id" to the graph.

        Does nothing if "id_num" in self._nodes and self._nodes[id_num].next_node_in_path != None
        """
        if next_node_id == -1:
            self._nodes[id_num] = _Node(id_num, [], [])
            return

        # add the next node w/o path if next node dne
        if next_node_id not in self._nodes:
            self._nodes[next_node_id] = _Node(next_node_id, [], [])

        # if origin node doesn't exist, add it w/ path. else, add path if not already set
        if id_num not in self._nodes:
            self._nodes[id_num] = _Node(id_num, [], [], self._nodes[next_node_id])
        else:
            if self._nodes[id_num].next_node_to_target is None:
                self._nodes[id_num].next_node_to_target = self._nodes[next_node_id]

    def get_nodes(self) -> list[_Node]:
        """
        Getter for _nodes. Returns a dictionary of id: _Node.
        """
        return list(self._nodes.values())


class Database:
    """
    A Database with a corresponding Graph representing all Wikipedia pages as vertices and
    all connecting hyperlinks as edges. Has functionality to correlate titles to pages IDs.

    Instance Attributes:
        - _titles: dict of page id number to title
        - _graph = directed graph representing the pages and links between them
    """
    _titles: dict[int, str]
    _graph: Graph

    def __init__(self, edge_file_path: str, title_file_path: str, use_edge_save_state: bool = False,
                 precompute: bool = True) -> None:
        # load titles from db and save in dict
        self._titles = self._load_titles(title_file_path)

        # builds the graph and populates paths by using bfs on whole graph
        if use_edge_save_state:
            self._graph = self._load_graph_from_save_state(edge_file_path)
        else:
            self._graph = self._load_graph(edge_file_path)
            if precompute:
                self._graph.compute_paths(1095706)

    def _load_titles(self, path: str) -> dict[int, str]:  # slow and bad but works
        """
        Using the data given from path, loads the Wikipedia page titles into a dict relating
        {id: name}
        """
        out_dict = {}
        with gzip.open(path, "r") as file:
            for line in file:
                data = str(line, 'utf-8').strip().split(" ")
                out_dict[int(data[0])] = str(data[1]).replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')
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

    def _load_graph_from_save_state(self, path: str) -> Graph:
        """
        Loads graph from a save state. This creates verticies for all pages in the dataset, but does not save all of the
        edges. Instead, it only populates the "next_node_in_path" variable, allowing for the fastest path calculations
        necessary for the "get_path" function to run.

        This is meant to save on memory usage and load time, and is not recommended for a hypothetical production
        deployment. However, considering loading the whole dataset and building the graph takes an hour and uses >14gb
        of ram (thanks hashtables!), this is necessary for a dataset of this size to run on anything short of a large
        server. We tried our best to optimize memory usage, but its really hard to load all of 2023 Wikipedia in a way
        that doesnt crush your dreams.
        """
        graph = Graph()
        with gzip.open(path, 'r') as file:
            for line in file:
                edge = str(line, "utf-8").strip().split(" ")
                if edge[0] == edge[1]:
                    graph.target_id = int(edge[0])
                graph.add_node_with_path(int(edge[0]), int(edge[1]))
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

    def get_path(self, id_num: int) -> list[int]:
        """Return a list of the id_num's of the shortest path to the target. Returns an empty
        list if this id_num is not connected to the target.

        Raise a ValueError if id_num is not in this dataset.
        """
        return self._graph.get_path(id_num)

    def make_save_state(self, file: FileIO) -> None:
        """Writes a save state file that saves the node id's and next nodes in path for all nodes in the graph.

        Used to make low memory dataset.
        """
        for node in self._graph.get_nodes():
            next_id = node.next_node_to_target.id_num if node.next_node_to_target is not None else -1
            file.write(f"{node.id_num} {next_id}\n")


if __name__ == '__main__':
    from tests import run_tests
    run_tests()
