from model import RationalLLM
from BeliefNet import DAG
from utils import cache_wrapper

def prompt_to_output_test(text, cache = {}):
    rationalLLM = RationalLLM()
    net = DAG()

    nodes = cache_wrapper(cache, 'nodes', rationalLLM.get_nodes, text)
    print('nodes')
    print(nodes)
    print()

    factors = cache_wrapper(cache, 'factors', rationalLLM.get_factors, nodes)
    print('factors')
    print(factors)
    print()

    factorsParsed = cache_wrapper(cache, 'factorsParsed', rationalLLM.factor_parsing, factors, nodes)
    print('factorsParsed')
    print(factorsParsed)
    print()

    for factor in factorsParsed:
        net.add_node(factor)

    edges = cache_wrapper(cache, 'edges', rationalLLM.get_edges, factorsParsed, nodes)
    print('edges')
    print(edges)
    print()

    for e in edges:
        net.add_edge(e[0], e[1])

    interpretations = cache_wrapper(cache, 'interpretations', rationalLLM.interpret_graph, net, text)
    print('interpretations')
    print(interpretations)
    print()

    output = cache_wrapper(cache, 'output', rationalLLM.to_Output, text, interpretations, nodes)
    print('output')
    print(output)
    print()

    return net, interpretations, cache

def prompt_to_output(text):
    rationalLLM = RationalLLM()
    net = DAG()

    nodes = rationalLLM.get_nodes(text)

    factors = rationalLLM.get_factors(nodes)

    factors = rationalLLM.factor_parsing(factors, nodes)

    for factor in factors:
        net.add_node(factor)

    edges = rationalLLM.get_edges(factors, nodes)

    for e in edges:
        net.add_edge(e[0], e[1])

    interpretations = rationalLLM.interpret_graph(net, text)

    output = rationalLLM.to_Output(text, interpretations, nodes)

    return net, output

def get_inferences(text):
    return prompt_to_output(text)[1]