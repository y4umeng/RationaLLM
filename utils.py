from openai import AzureOpenAI
from client import client

def get_response(message, instruction):
    response = client.chat.completions.create(
		model = 'gpt-35-turbo',
        temperature = 0,
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": message}
        ]
    )
    
    # print token usage
    # print(response.usage)

    return response.choices[0].message.content

def get_boolean_completion(text, statement):
    response = client.completions.create(
		model = 'gpt-35-turbo',
        prompt = f'Text: {text}\nYou are an expert labelling bot. Given the previous text, label the following statement with boolean value 0 or 1.\nStatement: {statement}\nLabel: ',
        temperature = 0,
        max_tokens = 1,
        seed = 8,
        logprobs = 2,
    )
    
    return response.choices[0].text, response.choices[0].logprobs.top_logprobs

def get_reasoning(text, statement):
    response = client.chat.completions.create(
        model = 'gpt-35-turbo',
        temperature = 0,
        messages = [
            {"role": "system", "content": text},
            {"role": "user", "content": f"{statement}. Explain the last statement with one fact."}
        ]
    )

    return response.choices[0].message.content

