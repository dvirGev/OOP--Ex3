# from _typeshed import Self
# from os import stat_result
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
import json

from codes.DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph=DiGraph()) -> None:
        super().__init__()
        self.graph = graph
        self.dijkstra = Dijkstra(graph)

    def updateDijkstra(self, src: int) -> None:
        if src != self.dijkstra.src or self.graph.mc != self.dijkstra.MC:
            self.dijkstra.src = src
            self.dijkstra.MC = self.graph.mc
            self.dijkstra.alg()

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            self.graph = DiGraph()
            with open(file_name, "r") as fp:
                di = json.load(fp)
                for node in di["Nodes"]:
                    id = node["id"]
                    if "pos" in node:
                        posData = node["pos"].split(',')
                        self.graph.add_node(
                            id, (float(posData[0]), float(posData[1]), float(posData[2])))
                    else:
                        self.graph.add_node(id)
                for edge in di["Edges"]:
                    self.graph.add_edge(edge["src"], edge["dest"], edge["w"])
        except:
            return False
        self.dijkstra.graph = self.graph
        return True

    def save_to_json(self, file_name: str) -> bool:
        dict = {"Nodes": [], "Edges": []}
        for node in self.graph.nodes.values():
            id = node.key
            if(node.location != None):
                pos = f'{node.location[0]},{node.location[1]},{node.location[2]}'
                dict["Nodes"].append({"id": id, "pos": pos})
            else:
                dict["Nodes"].append({"id": id})
            
        for edge in self.graph.edges.keys():
            dict["Edges"].append(
                {"src": edge[0], "dest": edge[1], "w": self.graph.edges[edge]})

        try:
            with open(file_name, 'w') as f:
                json.dump(dict, indent=2, fp=f)
        except:
            return False
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        self.updateDijkstra(id1)
        self.dijkstra.buildPath(id2)
        w = self.dijkstra.dist[id2]
        l = self.dijkstra.path[id2]
        return (w, l)

    # def TSP(self, node_lst: List[int]) -> (List[int], float):
    #     """
    #     Finds the shortest path that visits all the nodes in the list
    #     :param node_lst: A list of nodes id's
    #     :return: A list of the nodes id's in the path, and the overall distance
    #     """

    # def centerPoint(self) -> (int, float):
    #     """
    #     Finds the node that has the shortest distance to it's farthest node.
    #     :return: The nodes id, min-maximum distance
    #     """

    # def plot_graph(self) -> None:
    #     """
    #     Plots the graph.
    #     If the nodes have a position, the nodes will be placed there.
    #     Otherwise, they will be placed in a random but elegant manner.
    #     @return: None
    #     """
    #     raise NotImplementedError


class Dijkstra:
    def __init__(self, graph: GraphInterface) -> None:
        self.src = -1
        self.MC = -1
        self.dist = {}
        self.path = {}
        self.dads = {}
        self.graph = graph

    def initMaps(self, dads: dict, Q: list) -> None:
        for node in self.graph.nodes.keys():
            if node != self.src:
                self.dist[node] = float('inf')
                dads[node] = float('inf')
                Q.append(node)
                self.path[node] = []
        dads[self.src] = self.src
        self.dist[self.src] = 0.0
        self.path[self.src] = []
        Q.append(self.src)

    def minInList(self, Q: list) -> int:
        min2 = float('inf')
        ans = float('-inf')
        for node in Q:
            if min2 > self.dist[node]:
                ans = node
                min2 = self.dist[node]
        if ans != float('-inf'):
            Q.remove(ans)
        return ans

    def relax(self, src: int, dest: int) -> None:
        newDist = self.dist[src] + self.graph.edges[(src, dest)]
        if newDist < self.dist[dest]:
            self.dist[dest] = newDist
            self.dads[dest] = src

    def alg(self):
        Q = []
        self.initMaps(self.dads, Q)
        while len(Q) != 0:
            u = self.minInList(Q)
            if u == float('-inf'):
                return
            for dest in self.graph.all_out_edges_of_node(u).keys():
                self.relax(u, dest)

    def buildPath(self, dest: int) -> None:
        if len(self.path[dest]) != 0:
            return
        self.path[dest] = []
        if dest == self.src:
            self.path[dest].append(dest)
            return
        dad = self.dads[dest]
        if dad == float('inf'):
            return
        if dad in self.path:
            self.buildPath(dad)
        self.path[dest].extend(self.path[dad])
        self.path[dest].append(dest)
