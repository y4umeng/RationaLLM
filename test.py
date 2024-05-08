from openai import AzureOpenAI
from utils import get_response, get_boolean_completion
from model import RationaLLM
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

# message = """
# The United States will cross a historic threshold on Monday when for the first time a former president goes on criminal trial in a case laced with fateful significance because Donald Trump could be back in the Oval Office next year.

# When the presumptive GOP nominee walks into court for the start of jury selection, he and the country will enter a new state of reality as legal and political worlds collide in a trial almost guaranteed to deepen Americans’ bitter ideological estrangement.
# """
short_message = 'The United States will cross a historic threshold on Monday when for the first time a former president goes on criminal trial in a case laced with fateful significance because Donald Trump could be back in the Oval Office next year.' 
# # https://arxiv.org/pdf/2309.11392.pdf

paper_example = 'Heating ice will leave a puddle'
# earth = 'The earth is flat.'

class_example = "The United States on Sunday highlighted its role in helping Israel thwart Iran’s aerial attack as President Joe Biden convened leaders of the Group of Seven countries in an effort to prevent a wider regional escalation and coordinate a global rebuke of Tehran."
model = RationaLLM()
nodes = RationaLLM.get_nodes(class_example)
print(nodes)
print(RationaLLM.gen_parent(class_example, nodes[0], supporting=True))

# Trump said "We should help Isreal" is another entailment. 
#

# print(nodes)
# for n in nodes:
#     truth = get_completion(short_message, n)
#     print(f'{n}. Truth: {truth[0]}')
# print(get_completion("Trump was a good president"))



# a = BbnNode(Variable(0, 'a', ['on', 'off']), [0.5, 0.5])
# b = BbnNode(Variable(1, 'b', ['on', 'off']), [0.5, 0.5, 0.4, 0.6])

# a.probs = [0.2, 0.1]
# attrs = vars(a)
# print(', '.join("%s: %s" % item for item in attrs.items()))

# # create the network structure
# bbn = Bbn() \
#     .add_node(a) \
#     .add_node(b) \
#     .add_edge(Edge(a, b, EdgeType.DIRECTED)) 

# # convert the BBN to a join tree
# join_tree = InferenceController.apply(bbn)

# # insert an observation evidence
# ev = EvidenceBuilder() \
#     .with_node(join_tree.get_bbn_node_by_name('a')) \
#     .with_evidence('on', 1.0) \
#     .build()
# join_tree.set_observation(ev)

# # print the marginal probabilities
# for node in join_tree.get_bbn_nodes():
#     potential = join_tree.get_bbn_potential(node)
#     print(node)
#     print(potential)