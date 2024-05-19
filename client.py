from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = "https://hkust.azure-api.net",
  api_version = "2023-05-15",
  api_key = "74c6db8095f740e488467b96e4274094" #put your api key here
)
