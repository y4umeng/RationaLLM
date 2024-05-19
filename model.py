from openai import AzureOpenAI
from utils import get_response, get_boolean_completion, clean_text, get_opinion, get_span, get_list

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

    def get_nodes(self, text, size = 3):
        instruction = 'Extract a list of concise predicates from the text as a bulleted list'
        # instruction modified from https://arxiv.org/pdf/2309.11392.pdf
        #instruction = 'I want you to act as a language expert. Your task is to extract concise and relevant statements from the text. The truthfulness of the statement is irrelevant. Please only reply with the bullet list and nothing else.'
        #instruction = 'Extract a list of subjects and objects from the text'

        nodes = get_list(text, instruction)[:size]
            
        return nodes
    
    def factor_proposal(self, node):
        instructionChild = 'What factors are the implications of the phrase. Give only the title of each factor in a bullet list'
        instructionParent = 'What factors imply the phrase. Give only the title of each factor in a bullet list'

        children = get_list(node, instructionChild)
        parents = get_list(node, instructionParent)

        factors = parents + children

        #parents = [' '.join(line.split(':')[0].split(' ')[1:]) for line in parents.split('\n')[1:] if line != '']
        return factors, parents, children


    def factor_parsing(self, factors, nodes, size = 5):
        #instruction = remove bullet form:'
        #r = get_response(','.join(factors), instruction, 0.6)

        instruction = 'Condense the list into only' + str(size) + 'distinct factors and nothing else in a bullet form:'
        factors = get_list(','.join(factors), instruction)[:size]

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

    def get_edges(self, factors, nodes, threshold = 0.4):
        edges = []
        for f1 in factors:
            for f2 in nodes:
                edges.append([f1, f2, self.edge_probability(f1, f2)])

        edges.sort(key = lambda x: x[2], reverse = True)

        return [i for i in edges if i[-1] > threshold]

    def interpret_graph(self, graph, prompt, threshold = 0.2):
        interpretations = []
        for edge in graph.edges():
            try:
                statement = edge[0] + ' influences ' + edge[1]

                r = get_opinion(prompt, statement)
                confidence = graph.get_edge_data(edge[0], edge[1])['weight'] *r[1][r[0]]

                if r[0] != 1 and confidence > threshold:
                    if r[0] == 0:
                        statement += '. Text disagrees.'

                    else:#2
                        statement += '. Not said in text.'

                    interpretations.append([edge, statement, confidence])
            except:
                pass

        return interpretations

    def to_Output(self, prompt, interpretations, nodes):
        cache = {}
        output = []

        example = {"attribute": "unsaid",
                   "value": 1,
                   "explanation": "India may have stepped up surveillance due to an increase in cases in whole of Asia. Not said in prompt.",
                   "span": [[151, 230]],
                   "confidence": 0.9}

        instruction = prompt + ' :Text. Choose a sentence from the text that best represents the statement. Return only the sentence in the text exactly as it appears: '
        for edge, comment, confidence in interpretations:
            #find span
            if edge[0] in nodes:
                node = edge[0]
            else:
                node = edge[1]

            if node in cache:
                span = cache[node]
            else:
                instruction = 'Return ONLY a section from the prompt that best shows the statement "' + node + '": Return only a substring of the prompt nothing else'
                try:
                    r = get_response(prompt, instruction, 0.6)
    
                    span = get_span(prompt, r)
                except:
                    span = [0, len(prompt) - 1]

                cache[node] = span


            output.append({})

            output[-1]["attribute"] = example["attribute"]
            output[-1]["value"] = example["value"]
            output[-1]["explanation"] = comment
            output[-1]["span"] = [span]
            output[-1]["confidence"] = f'{confidence:.2f}'

        return output


