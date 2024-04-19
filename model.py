import pybbn
from openai import AzureOpenAI
from utils import get_response, get_boolean_completion, clean_text

class RationalLLM():
    """
        Model
    """
    def __init__(self):
        # self.leaves = self.get_nodes(text)
        # self.graphs = []
        # for node in self.leaves:
        #     graph_size = 1
        #     while graph_size < 10:
        pass

    def get_nodes(self, text):
        # instruction modified from https://arxiv.org/pdf/2309.11392.pdf
        #instruction = 'Split the sentence into bulleted predicates'
        instruction = 'I want you to act as a language expert. Your task is to extract concise and relevant statements from the text. The truthfulness of the statement is irrelevant. Please only reply with the bullet list and nothing else.'
        response = get_response(text, instruction, 0)
        unformatted_nodes = response.split('\n')
        nodes = [clean_text(text) for text in unformatted_nodes]
            
        return nodes

    def gen_parent(text, child, supporting=True):
        if supporting:
            instruction = f'You believe everything in the following text to be true. {text}'
            message = f"{child}. Explain the last statement with a 2-step reasoning chain. Each step must be a short statement."
        else:
            instruction = f'You believe everything in the following text to be false. {text}'
            message = f"{child}. Explain why the the last statement is false with a 2-step reasoning chain. Each step must be a short factual statement."
        
        parent = get_response(message, instruction, 0.6)

        # formatting
        parent = parent.split('\n')[0].split(':')[-1].strip()
        punc = ".,!?"
        if parent[-1] in punc: parent = parent[:-1]

        # check if model believes parent implies child
        response = get_boolean_completion(f'{parent[:-1]}. This implies that {child}.')
        if response == None: return None

        truth_val, probs = response
        return parent, probs
    
    def factor_proposal(self, node):
        instructionChild = 'What factors are the implications of the phrase. Give only the title of each factor in a bullet list'
        instructionParent = 'What factors imply the phrase. Give only the title of each factor in a bullet list'

        children = get_response(node, instructionChild, 0.6)
        parents = get_response(node, instructionParent, 0.6)

        children = [clean_text(i) for i in children.split('\n')]
        parents = [clean_text(i) for i in parents.split('\n')]

        factors = parents + children

        #parents = [' '.join(line.split(':')[0].split(' ')[1:]) for line in parents.split('\n')[1:] if line != '']
        return factors, parents, children


    def factor_parsing(self, factors, nodes, size = 5):
        instruction = 'Condense the list into only' + str(size) + 'distinct factors and nothing else in a bullet form:'
        r = get_response(','.join(factors), instruction, 0.6)

        factors = [clean_text(i) for i in r.split('\n')]

        return factors + nodes

    def get_factors(self, nodes):
        factorsSeparate = []
        factors = []
        for n in nodes:
            p = self.factor_proposal(n)
            factorsSeparate.append(p)
            factors.extend(p[0])

        return factors

    def edge_probability(self, u, v):
        instruction = 'On a scale of 1 to 5, how true is this sentence. give only a number nothing else:'
        text = u + ' influences ' + v
        r = get_response(text, instruction, 0.6)
        try:
            return int(r)/5
        except:
            return 0

    def get_edges(self, factors, threshold = 0.4):
        edges = []
        for f1 in factors:
            for f2 in factors:
                if f1 != f2:
                    edges.append([f1, f2, self.edge_probability(f1, f2)])

        edges.sort(key = lambda x: x[2], reverse = True)
        print(edges)

        return [i for i in edges if i[-1] > threshold]

    def compare_prompt(self, prompt, edge):
        statement = edge[0] + ' influences ' + edge[1]
        return get_boolean_completion(statement, prompt)

    def interpret_graph(self, graph, prompt, threshold = 0.2):
        interpretations = []
        for edge in graph.edges():
            r = self.compare_prompt(prompt, edge)
            if r[1][1] < threshold:
                interpretations.append(edge[0] + ' also influences ' + edge[1])
            else:
                print('!!', edge)

        return interpretations




