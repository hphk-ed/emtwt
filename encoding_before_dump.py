import json

with open('dump.json', 'r', encoding='cp949') as f:
    decoded_data = json.load(f)
    with open('decoded_data.json', 'w', encoding='utf-8' , newline='') as rf:
        json.dump(decoded_data, rf, indent=2, ensure_ascii=False)