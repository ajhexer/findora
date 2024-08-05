import json


def load_docs(path, fields_to_retain):
    with open(path, 'r') as f:
        raw_docs = json.load(f)
        docs = {key: {field: value[field] for field in fields_to_retain} for key, value in raw_docs.items()}
    return docs


