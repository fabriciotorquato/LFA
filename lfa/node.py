class Node():
    def __init__(self, name, is_final_node=False, is_initial_node=False):
        self.name = name
        self.edges = []
        self.is_final_node = is_final_node
        self.is_initial_node = is_initial_node
