class Node():
    def __init__(self,name,is_final_node = False):
        self.name = name
        self.edges = []
        self.is_final_node = is_final_node