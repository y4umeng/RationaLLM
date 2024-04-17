import pybbn
from openai import AzureOpenAI
from utils import get_response, get_boolean_completion

class RationaLLM():
    """
        Model
    """
    def __init__(self):
        pass

    def get_nodes(text):
        # instruction modified from https://arxiv.org/pdf/2309.11392.pdf
        instruction = 'I want you to act as a language expert. Your task is to extract concise and relevant statements from the text. The truthfulness of the statement is irrelevant. Please only reply with the bullet list and nothing else.'
        response = get_response(text, instruction, 0)
        unformatted_nodes = response.split('\n')
        nodes = []
        punc = ".,!?"
        for n in unformatted_nodes:
            n = n.strip()
            if n[-1] in punc: n = n[:-1]
            while len(n) and not n[0].isalpha(): n = n[1:]
            if len(n) > 3: nodes.append(n)
            
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
    

        
    
