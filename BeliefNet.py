from openai import AzureOpenAI
from pybbn.graph.dag import Bbn

class BeliefNetwork():
    network = None
    def __init__():
        network = Bbn()

    def add(node):
        network
        pass

from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

# create the nodes
a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])
c = BbnNode(Variable(2, 'c', ['on', 'off']), [0.7, 0.3, 0.2, 0.8])
d = BbnNode(Variable(3, 'd', ['on', 'off']), [0.9, 0.1, 0.5, 0.5])
e = BbnNode(Variable(4, 'e', ['on', 'off']), [0.3, 0.7, 0.6, 0.4])
f = BbnNode(Variable(5, 'f', ['on', 'off']), [0.01, 0.99, 0.01, 0.99, 0.01, 0.99, 0.99, 0.01])
g = BbnNode(Variable(6, 'g', ['on', 'off']), [0.8, 0.2, 0.1, 0.9])
h = BbnNode(Variable(7, 'h', ['on', 'off']), [0.05, 0.95, 0.95, 0.05, 0.95, 0.05, 0.95, 0.05])

# create the network structure
bbn = Bbn() \
    .add_node(a) \
    .add_node(b) \
    .add_node(c) \
    .add_node(d) \
    .add_node(e) \
    .add_node(f) \
    .add_node(g) \
    .add_node(h) \
    .add_edge(Edge(a, b, EdgeType.DIRECTED)) \
    .add_edge(Edge(a, c, EdgeType.DIRECTED)) \
    .add_edge(Edge(b, d, EdgeType.DIRECTED)) \
    .add_edge(Edge(c, e, EdgeType.DIRECTED)) \
    .add_edge(Edge(d, f, EdgeType.DIRECTED)) \
    .add_edge(Edge(e, f, EdgeType.DIRECTED)) \
    .add_edge(Edge(c, g, EdgeType.DIRECTED)) \
    .add_edge(Edge(e, h, EdgeType.DIRECTED)) \
    .add_edge(Edge(g, h, EdgeType.DIRECTED))

# convert the BBN to a join tree
join_tree = InferenceController.apply(bbn)

# insert an observation evidence
ev = EvidenceBuilder() \
    .with_node(join_tree.get_bbn_node_by_name('a')) \
    .with_evidence('on', 1.0) \
    .build()
join_tree.set_observation(ev)

# print the marginal probabilities
for node in join_tree.get_bbn_nodes():
    potential = join_tree.get_bbn_potential(node)
    print(node)
    print(potential)

from pybbn.graph.dag import BbnUtil
from pybbn.graph.jointree import EvidenceBuilder, EvidenceType
from pybbn.pptc.inferencecontroller import InferenceController
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

np.random.seed(37)
plt.style.use('ggplot')
Marginal = namedtuple('Marginal', 'name, s')

def potential_to_series(p):
    vals = []
    index = []

    for pe in p.entries:
        try:
            v = pe.entries.values()[0]
        except:
            v = list(pe.entries.values())[0]
        p = pe.value

        vals.append(p)
        index.append(v)

    return pd.Series(vals, index=index)

def get_marginals(join_tree):
    data = []
    for node in join_tree.get_bbn_nodes():
        name = node.variable.name
        s = potential_to_series(join_tree.get_bbn_potential(node))
        t = Marginal(name, s)
        data.append(t)
    return data

# get the pre-defined huang graph
bbn = BbnUtil.get_huang_graph()

# convert the BBN to a join tree
join_tree = InferenceController.apply(bbn)

import math
from ipywidgets import interact

@interact(a=[('unobserved', -1), ('off', 0), ('on', 1)])
def f(a=-1):
    n_cols = 4
    n_rows = math.ceil(len(bbn.get_nodes()) / n_cols)

    if a == -1:
        join_tree.unobserve_all()
        marginals = get_marginals(join_tree)
    else:
        v = 'on' if a == 1 else 'off'
        ev = EvidenceBuilder() \
            .with_node(join_tree.get_bbn_node_by_name('a')) \
            .with_evidence(v, 1.0) \
            .build()
        join_tree.unobserve_all()
        join_tree.set_observation(ev)
        marginals = get_marginals(join_tree)

    marginals = sorted(marginals, key=lambda tup: tup[0])

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5), sharey=True)

    for m, ax in zip(marginals, np.ravel(axes)):
        m.s.plot(kind='bar', legend=False, ax=ax)
        ax.set_title(m.name)
        ax.set_ylim([0.0, 1.0])
        ax.set_xlabel('')

    plt.tight_layout()