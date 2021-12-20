class Node:
    def __init__(self, key: int, location: tuple) -> None:
        self.key = key
        self.location = location
        self.tag = 0
        self.fromMe = {}
        self.toMe = {}
    
    # def __init__(self, other: type(Node)) -> None:
    #     self.key = other.key
    #     self.location = other.location
    #     self.tag = other.tag
    