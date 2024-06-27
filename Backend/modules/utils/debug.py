import json

def dump_json(data):
    """this is just for debugging"""
    file = open("webhooks_data.json", "a")
    print(json.dumps(data, indent=4), file=file)