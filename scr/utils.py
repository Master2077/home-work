import json
import os

def load_operations(filename='operations.json'):
    base_dir = os.path.dirname(__file__)              # utils/
    data_path = os.path.join(base_dir, '..', 'data', filename)
    data_path = os.path.normpath(data_path)          # корректирует ../
    try:
        with open(data_path, encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


print(json.dumps(load_operations(), ensure_ascii=False, indent=2))