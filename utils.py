from openai import AzureOpenAI
from client import client
from math import exp

def get_response(message, instruction, temp):
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
        prompt = f'You are an expert labelling bot. Label the following statement with boolean value 0 or 1 indicating its truthfulnes.\nStatement: {statement}\nLabel: ', 
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



