import requests
import json
import csv
def fetch_data(path):
    try:
        response = requests.get(path, timeout=10)
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data from {path}: {e}")
        return None

def validate_data(data):
    if not isinstance(data[:1], list):
        print("Data is not a list.")
        return False
    for row in data:
        if row[0] is None:
            print(f"Invalid data found in row: {row}")
            return False
        if row[1] is None:
            print(f"Invalid data found in row: {row}")
            return False
        if row[2] is None or row[2].get('key') is None:
            print(f"Invalid data found in row: {row}")
            return False
    return True

def transform_data(data):
    transformed_data = []
    for row in data:
        if 'UserId' in row and 'Id' in row and 'Title' in row:
            transformed_data.append({
                'UserId': row['UserId'],
                'Id': row['Id'],
                'Title': row['Title'],
            })
    return transformed_data

def save_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def save_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

path = "https://dummyjson.com/"

data = fetch_data(path)
if data is not None:
    if validate_data(data):
        transformed_data = transform_data(data)
        save_json(transformed_data, "output.json")
        save_csv(transformed_data, "output.csv")