from model import RationalLLM
from utils import get_response, get_boolean_completion
from BeliefNet import BeliefNetwork

rationalLLM = RationalLLM()
instructionChild = 'What factors are the implications of the sentence. Give only the title of each factor in a bullet list'
instruction = 'What factors imply the sentence. Give only the title of each factor in a bullet list'
texts = ['Eating meat causes cancer',
'Brexit would not have passed if the entire population had voted',
]
'The chicken came before the egg'
# nodes = []
# for text in texts:
#     nodes.append(rationalLLM.get_nodes(text))

# print(nodes)
nodes = [['Eating meat', 'Causes cancer'], ['Brexit would not have passed', 'The entire population had voted'], ['The chicken came', 'The egg came after the chicken']]
print(nodes)

# factors = []
# for node in nodes:
#     factors.append([])
#     for n in node:
#         factors[-1].append(rationalLLM.factor_proposal(n))
# print(factors)
factors = [[(['cultural and social norms', 'personal beliefs and values', 'health concerns', 'environmental impact', 'availability and accessibility', 'dietary preferences and taste', 'health implications', 'environmental implications', 'ethical implications', 'cultural implications', 'economic implications'], ['cultural and social norms', 'personal beliefs and values', 'health concerns', 'environmental impact', 'availability and accessibility', 'dietary preferences and taste'], ['health implications', 'environmental implications', 'ethical implications', 'cultural implications', 'economic implications']), (['genetics', 'environmental pollutants', 'radiation exposure', 'tobacco use', 'alcohol consumption', 'poor diet and physical inactivity', 'viral infections', 'occupational hazards', 'hormonal imbalances', 'chronic inflammation', 'as an ai language model i am not sure which phrase you are referring to can you please provide me with the phrase'], ['genetics', 'environmental pollutants', 'radiation exposure', 'tobacco use', 'alcohol consumption', 'poor diet and physical inactivity', 'viral infections', 'occupational hazards', 'hormonal imbalances', 'chronic inflammation'], ['as an ai language model i am not sure which phrase you are referring to can you please provide me with the phrase'])], [(['factors that imply the phrase brexit would not have passed', '', 'the impact of misinformation and propaganda during the campaign', 'the lack of clarity and understanding about the consequences of leaving the eu', 'the narrow margin of victory for leave and the high number of undecided voters', 'the failure of the remain campaign to effectively communicate the benefits of eu membership', 'the role of immigration as a divisive issue in the referendum', 'the potential influence of external factors such as russian interference or the cambridge analytica scandal', 'political climate', 'demographics', 'economic factors', 'media influence', 'campaign strategies'], ['factors that imply the phrase brexit would not have passed', '', 'the impact of misinformation and propaganda during the campaign', 'the lack of clarity and understanding about the consequences of leaving the eu', 'the narrow margin of victory for leave and the high number of undecided voters', 'the failure of the remain campaign to effectively communicate the benefits of eu membership', 'the role of immigration as a divisive issue in the referendum', 'the potential influence of external factors such as russian interference or the cambridge analytica scandal'], ['political climate', 'demographics', 'economic factors', 'media influence', 'campaign strategies']), (['factors that imply the phrase the entire population had voted', '', 'universal suffrage', 'high voter turnout', 'accessible polling stations', 'efficient electoral administration', 'minimal voter suppression or intimidation', 'adequate voter education and awareness', 'increased democratic participation', 'accurate representation of the will of the people', 'potential for higher voter turnout', 'greater legitimacy of election results'], ['factors that imply the phrase the entire population had voted', '', 'universal suffrage', 'high voter turnout', 'accessible polling stations', 'efficient electoral administration', 'minimal voter suppression or intimidation', 'adequate voter education and awareness'], ['increased democratic participation', 'accurate representation of the will of the people', 'potential for higher voter turnout', 'greater legitimacy of election results'])], [(['sorry but i need more context to understand which factors you are referring to please provide more information about the phrase or sentence', 'im sorry but the phrase the chicken came is incomplete and lacks context it is not clear what implications or factors are being referred to can you please provide more information or context so i can assist you better'], ['sorry but i need more context to understand which factors you are referring to please provide more information about the phrase or sentence'], ['im sorry but the phrase the chicken came is incomplete and lacks context it is not clear what implications or factors are being referred to can you please provide more information or context so i can assist you better']), (['factors suggesting that the egg came after the chicken', '', 'evolutionary history', 'genetic mutations', 'natural selection', 'reproductive adaptations', 'evolutionary biology', 'genetics', 'reproduction', 'philosophy of causation', 'linguistics and semantics'], ['factors suggesting that the egg came after the chicken', '', 'evolutionary history', 'genetic mutations', 'natural selection', 'reproductive adaptations'], ['evolutionary biology', 'genetics', 'reproduction', 'philosophy of causation', 'linguistics and semantics'])]]

for i in range(len(nodes)):
    for j in range(len(nodes[i])):
        print(nodes[i][j], ':')
        print('parents:')
        [print('    ', i) for i in factors[i][j][1]]
        print('children:')
        [print('    ', i) for i in factors[i][j][2]]

factors0 = []
for factor in factors[0]:
    factors0.extend(factor[0])

# factors0 = rationalLLM.factor_parsing(factors0) + nodes[0]
# print(factors0)
factors0 = ['cultural and social norms', 'health concerns', 'availability and accessibility', 'dietary preferences and taste', 'environmental impact', 'Eating meat', 'Causes cancer']

net = BeliefNetwork()
for factor in factors0:
    net.add(factor)

# edges = []
# for f1 in factors0:
#     for f2 in factors0:
#         if f1 != f2:
#             edges.append([f1, f2, rationalLLM.edge_probability(f1, f2)])
# print(edges)
edges = [['cultural and social norms', 'health concerns', 0.8], ['cultural and social norms', 'availability and accessibility', 0.8], ['cultural and social norms', 'dietary preferences and taste', 1.0], ['cultural and social norms', 'environmental impact', 0.8], ['cultural and social norms', 'Eating meat', 0.6], ['cultural and social norms', 'Causes cancer', 0], ['health concerns', 'cultural and social norms', 0.8], ['health concerns', 'availability and accessibility', 0.8], ['health concerns', 'dietary preferences and taste', 0.8], ['health concerns', 'environmental impact', 0], ['health concerns', 'Eating meat', 0.6], ['health concerns', 'Causes cancer', 0.6], ['availability and accessibility', 'cultural and social norms', 0.8], ['availability and accessibility', 'health concerns', 0.6], ['availability and accessibility', 'dietary preferences and taste', 0.8], ['availability and accessibility', 'environmental impact', 0.8], ['availability and accessibility', 'Eating meat', 0.6], ['availability and accessibility', 'Causes cancer', 0.4], ['dietary preferences and taste', 'cultural and social norms', 0.8], ['dietary preferences and taste', 'health concerns', 0.8], ['dietary preferences and taste', 'availability and accessibility', 0], ['dietary preferences and taste', 'environmental impact', 0], ['dietary preferences and taste', 'Eating meat', 0.6], ['dietary preferences and taste', 'Causes cancer', 0.2], ['environmental impact', 'cultural and social norms', 0.8], ['environmental impact', 'health concerns', 1.0], ['environmental impact', 'availability and accessibility', 0], ['environmental impact', 'dietary preferences and taste', 0.6], ['environmental impact', 'Eating meat', 0.8], ['environmental impact', 'Causes cancer', 0.6], ['Eating meat', 'cultural and social norms', 0.6], ['Eating meat', 'health concerns', 0.6], ['Eating meat', 'availability and accessibility', 0.6], ['Eating meat', 'dietary preferences and taste', 0.8], ['Eating meat', 'environmental impact', 0.8], ['Eating meat', 'Causes cancer', 0.6], ['Causes cancer', 'cultural and social norms', 0.6], ['Causes cancer', 'health concerns', 0.6], ['Causes cancer', 'availability and accessibility', 0.6], ['Causes cancer', 'dietary preferences and taste', 0.4], ['Causes cancer', 'environmental impact', 0.6], ['Causes cancer', 'Eating meat', 0.6]]

edges.sort(key = lambda x: x[2], reverse=True)
[print(i) for i in edges]

threshold = 0.4
for e in edges:
    if e[2] > threshold:
        net.add_edge(e[0], e[1])
    else:
        break

net.display()

print(4)