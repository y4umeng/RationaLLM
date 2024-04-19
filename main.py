from model import RationalLLM
from BeliefNet import BeliefNetwork
from utils import cache_wrapper

def prompt_to_output_test(text, cache = {}):
    rationalLLM = RationalLLM()
    net = BeliefNetwork()

    nodes = cache_wrapper(cache, 'nodes', rationalLLM.get_nodes, text)
    print('nodes')
    print(nodes)

    factors = cache_wrapper(cache, 'factors', rationalLLM.get_factors, nodes)
    print('factors')
    print(factors)

    factorsParsed = cache_wrapper(cache, 'factorsParsed', rationalLLM.factor_parsing, factors, nodes)
    print('factorsParsed')
    print(factorsParsed)

    for factor in factorsParsed:
        net.add(factor)

    edges = cache_wrapper(cache, 'edges', rationalLLM.get_edges, factorsParsed)
    print('edges')
    print(edges)

    for e in edges:
        net.add_edge(e[0], e[1])

    return net, cache

def prompt_to_output(text):
    rationalLLM = RationalLLM()
    net = BeliefNetwork()

    nodes = rationalLLM.get_nodes(text)

    factors = rationalLLM.get_factors(nodes)

    factors = rationalLLM.factor_parsing(factors, nodes)

    for factor in factors:
        net.add(factor)

    edges = rationalLLM.get_edges(factors)

    for e in edges:
        net.add_edge(e[0], e[1])

    return net