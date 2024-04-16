import pybbn
from openai import AzureOpenAI
from utils import get_response, get_boolean_completion

class RationaLLM():
    """
        Model
    """
    def __init__(self):
        self.hi = 'hi'

    def get_nodes(text):
        # instruction modified from https://arxiv.org/pdf/2309.11392.pdf
        instruction = 'I want you to act as a language expert. Your task is to extract concise and relevant factual statements from the text. Include only statements that have a truth value and are worth validating, and ignore subjective claims. You should generate a bullet list of statements that are potentially true or false. Please only reply with the bullet list and nothing else.'
        response = get_response(text, instruction)
        unformatted_nodes = response.split('\n')
        nodes = []
        punc = ".,!?"
        for n in unformatted_nodes:
            n = n.strip()
            if n[-1] in punc: n = n[:-1]
            while len(n) and not n[0].isalpha(): n = n[1:]
            if len(n) > 3: nodes.append(n)
            
        return nodes
    
    def edge_finder(text, node1, node2):
        statement1 = f'The fact that {node1} implies that {node2}'
        statement2 = f'The fact that {node2} implies that {node1}'
        response = get_boolean_completion(text, statement1)
        if response[0] == '1': return 1
        response = get_boolean_completion(text, statement2)
        if response[0] == '1': return 2
        return 0
    
    def gen_parent(text, child):
        pass

        
    
