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

    def show_graph(self):
        nx.draw(self.network, with_labels=True)