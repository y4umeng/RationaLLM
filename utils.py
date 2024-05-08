from openai import AzureOpenAI
from client import client
from math import exp


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
    if text: 
        prompt = f'Text: {text}\nYou are an expert labelling bot. Given the previous text, label the following statement with boolean value 0 or 1.\nStatement: {statement}\nLabel: '
    else:
        prompt = f'You are an expert labelling bot. Label the following statement with boolean value 0 or 1 indicating its truthfulnes.\nStatement: {statement}\nLabel: '
    response = client.completions.create(
        model = 'gpt-35-turbo',
        prompt = prompt,
        temperature = 0,
        max_tokens = 1,
        seed = 8,
        logprobs = 2,
    )

    # assert answer is 0 or 1
    answer = response.choices[0].text
    if answer != '0' and answer != '1': return None

    # format logprobs and calculate probabilities
    logprobs = response.choices[0].logprobs.top_logprobs[0]
    if '1' in logprobs and '0' in logprobs:
        log0 = exp(logprobs['0'])
        log1 = exp(logprobs['1'])
        sum = log0 + log1
        return int(answer), [log0/sum, log1/sum]
    return None

#Say whether the statement is inferencable by the text
def get_opinion(statement, text):
    prompt = 'Text:' + text + 'You are an expert labelling bot. Given only the previous text, label the following statement with: 0 - the text directly disagrees with the statement, 1 - the text directly agrees with the statement, 2 - the text does not directly give any opinion. return only 0,1 or 2. Statement: ' + statement + 'Label: '

    response = client.completions.create(
		model = 'gpt-35-turbo',
        prompt = prompt,
        temperature = 0,
        max_tokens = 1,
        seed = 8,
        logprobs = 3,
    )

    # Assert answer is valid
    answer = response.choices[0].text
    if answer not in list('012'): return None

    logprobs = response.choices[0].logprobs.top_logprobs[0]
    if False in [i in logprobs for i in list('012')]: return None

    # format logprobs and calculate probabilities
    log0 = exp(logprobs['0'])
    log1 = exp(logprobs['1'])
    log2 = exp(logprobs['2'])
    sum = log0 + log1 + log2

    return int(answer), [log0/sum, log1/sum, log2/sum]

# Other utils
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