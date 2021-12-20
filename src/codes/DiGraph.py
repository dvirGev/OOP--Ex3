from GraphInterface import GraphInterface
from codes.Node import Node

class DiGraph(GraphInterface):
    def __init__(self) -> None:
        super().__init__()
        self.nodes = {}
        self.edges = {}
        self.mc = 0
    
    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return len(self.edges)

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.nodes[id1].toMe

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.nodes[id1].fromMe

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if(not id1 in self.nodes.keys()) or (not id2 in self.nodes.keys()):
            return False
        self.edges[(id1,id2)] = weight
        self.nodes[id1].fromMe[id2] = weight
        self.nodes[id2].toMe[id1] = weight
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes.keys():
            return False
        self.nodes[node_id] = Node(node_id,(pos))
        self.mc += 1
        return True
        

    def remove_node(self, node_id: int) -> bool:
        if not node_id in self.nodes.keys():
            return False
        for src in self.nodes[node_id].toMe.keys():
            self.edges.pop((src, node_id))
            self.nodes[src].fromMe.pop(node_id)
        for dest in self.nodes[node_id].fromMe.keys():
            self.edges.pop((node_id, dest))
            self.nodes[dest].toMe.pop(node_id)
        self.nodes.pop(node_id)
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if (not node_id1 in self.nodes.keys()) or (not node_id2 in self.nodes.keys()) or (not (node_id1, node_id2) in self.edges.keys()):
            return False
        self.edges.pop((node_id1, node_id2))
        self.nodes[node_id1].fromMe.pop(node_id2)
        self.nodes[node_id2].toMe.pop(node_id1)
        self.mc += 1
        return True
    
    