import networkx as nx
import matplotlib.pyplot as plt

class DAG(nx.DiGraph):
    def __init__(self):
        super().__init__()

    def add_edge(self, a, b, confidence = 0.5):
        super().add_edge(a, b, weight=confidence)
        if not nx.is_directed_acyclic_graph(self):
            self.remove_edge(a, b)

    def display(self):
        nx.draw(self, with_labels=True)
        plt.draw()