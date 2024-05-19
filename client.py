from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2023-05-15",
  api_key = "" #put your api key here
)
