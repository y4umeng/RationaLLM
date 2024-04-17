from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2023-05-15",
  api_key = "a6df25842ae4400db362c11744abc570" #put your api key here
)
