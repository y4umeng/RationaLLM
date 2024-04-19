import pybbn
from openai import AzureOpenAI
from utils import get_response, get_boolean_completion, clean_text

class RationalLLM():
    """
        Model
    """
    def __init__(self):
        pass

    def get_nodes(self, text):
        # instruction modified from https://arxiv.org/pdf/2309.11392.pdf
        instruction = 'Split the sentence into bulleted predicates'
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

        children = get_response(instructionChild, node, 0.6)
        parents = get_response(instructionParent, node, 0.6)

        children = [clean_text(i) for i in children.split('\n')]
        parents = [clean_text(i) for i in parents.split('\n')]

        factors = parents + children

        #parents = [' '.join(line.split(':')[0].split(' ')[1:]) for line in parents.split('\n')[1:] if line != '']
        return factors, parents,children

    def factor_parsing(self, factors, size = 5):
        instruction = 'Condense the list into only' + str(size) + 'distinct factors and nothing else in a bullet form:'
        r = get_response(instruction, ','.join(factors), 0.6)

        factors = [clean_text(i) for i in r.split('\n')]

        return factors

    def edge_probability(self, u, v):
        instruction = 'On a scale of 1 to 5, how true is this sentence. give only a number nothing else:'
        text = u + ' influences ' + v
        r = get_response(instruction, text, 0.6)
        try:
            return int(r)/5
        except:
            return 0

    def compare_prompt(self, prompt, edge):
        pass
