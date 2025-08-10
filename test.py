from load import get_context
from llm_and_route_query import prompt

response = get_context("YTUFAQ", "ဆရာမတွေ စာသင်တာကောင်းလား", prompt['FAQ'], [])
print(response['answer'])