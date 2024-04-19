from openai import AzureOpenAI
from pybbn.graph.dag import Bbn
import networkx as nx
import matplotlib.pyplot as plt

class BeliefNetwork():
    network = None
    def __init__(self):
        self.network = nx.DiGraph()

    def add(self, node):
        self.network.add_node(node)

    def add_edge(self, a, b):
        self.network.add_edge(a, b)
        if not nx.is_directed_acyclic_graph(self.network):
            self.network.remove_edge(a, b)

    def display(self):
        nx.draw(self.network, with_labels=True)
        plt.draw()