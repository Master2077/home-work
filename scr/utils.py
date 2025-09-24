import json
import os

def load_operations():
    try:
        with open('../data/operations.json', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


print(json.dumps(load_operations(), ensure_ascii=False, indent=2))