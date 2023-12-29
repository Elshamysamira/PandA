import requests
import json
from shakespeare import Sonnet, Index, Query

url = "https://poetrydb.org/author,title/Shakespeare;Sonnet"
response = requests.get(url)

if response.status_code == 200:
    print("Request was successful!")
    print("Response content:")
    data = json.loads(response.text)

shakespeare_sonnets = [Sonnet(sonnet_dict) for sonnet_dict in data]
shakespeare_index = Index(shakespeare_sonnets)

while True:
    user_input = input("Search for sonnets ('q' to quit)")
    if user_input == "q":
        break
    user_query = Query(user_input)
    matching_sonnets = shakespeare_index.search(user_query)
    sonnet_ids = [sonnet.id for sonnet in matching_sonnets]
    print(f"--> Your search for '{user_input}' matched {len(matching_sonnets)} sonnets {sonnet_ids}:")
    for sonnet in matching_sonnets:
        print(sonnet)