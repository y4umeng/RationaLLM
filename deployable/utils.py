from openai import AzureOpenAI
from client import client
from math import exp

from transformers import pipeline

classifier = pipeline("text-classification", model = "microsoft/deberta-large-mnli")


# LLM wrappers ------------------------------
def get_response(message, instruction, temp = 0.6):
    response = client.chat.completions.create(
		 model = 'gpt-35-turbo',
        temperature = temp,
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": message}
        ]
    ) 
    # print token usage
    # print(response.usage)

    return response.choices[0].message.content

def get_boolean_completion(statement, text=None):
    if not text:
        raise 'this functionality is not implemented'

    inference = classifier('[CLS]' + text + '[SEP]' + statement + '[SEP]')[0]

    #Set the complement probability
    log0 = (1-inference['score'])
    log1 = (1-inference['score'])

    #Set the chosen class
    if inference['label'] == 'ENTAILMENT':
        log1 = inference['score']
        answer = 1
    else:
        log0 = inference['score']
        answer = 0

    return answer, [log0, log1]

#Say whether the statement is inferencable by the text
def get_opinion(statement, text):
    inference = classifier('[CLS]' + text + '[SEP]' + statement + '[SEP]')[0]

    #Split the complement probability
    log0 = (1-inference['score'])/2
    log1 = (1-inference['score'])/2
    log2 = (1-inference['score'])/2

    #Set the chosen class
    if inference['label'] == 'CONTRADICTION':
        log0 = inference['score']
        answer = 0
    elif inference['label'] == 'ENTAILMENT':
        log1 = inference['score']
        answer = 1
    elif inference['label'] == 'NEUTRAL':
        log2 = inference['score']
        answer = 2

    return int(answer), [log0, log1, log2]

#Wrapper for parsing what the LLM give

def get_list(text, instruction):
    response = get_response(text, instruction, 0)
    rawElements = response.split('\n')

    #clean LLM mess:
    elements = [clean_text(text) for text in rawElements]

    elements = [text for text in elements if not_mess(text)]

    return elements

# Other utils
def not_mess(text):
    mess = ['']
    if text in mess:
        return False

    messSegments = ['As an AI language model']
    for messSegment in messSegments:
        if text in messSegment:
            return False

    return True

def clean_text(text):
    return ''.join([char for char in text.lower() if ord(char) >= 97 and ord(char) <= 122 or char == ' ']).strip()

def cache_wrapper(cache, name, function, *argv):
    if name not in cache:
        cache[name] = function(*argv)

    return cache[name]

def get_span(text, subtext):
    cleanSub = clean_text(subtext)
    start = clean_text(text).index(cleanSub)
    return [start, start + len(cleanSub)]