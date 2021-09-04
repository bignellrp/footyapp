import json

def lookup(value):
    path_to_token = "../tokens/tokens.json"
    with open(path_to_token, "r") as handler:
        info = json.load(handler)
    return info[value]