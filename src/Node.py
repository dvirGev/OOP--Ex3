class Node:
    def __init__(self, key: int, location = ()) -> None:
        self.key = key
        self.location = location
        self.tag = 0
        self.fromMe = {}
        self.toMe = {}
    def __repr__(self) -> str:
        return f'Key: {self.key}, Location {self.location}'
    
    # def __init__(self, other: type(Node)) -> None:
    #     self.key = other.key
    #     self.location = other.location
    #     self.tag = other.tag
    