import requests
import json
import csv
import logging
logging.basicConfig(filename='logs/pipeline.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_data(path):
    try:
        logging.info(f"Fetching data from {path}")
        response = requests.get(path, timeout=10)
        data = response.json()
        logging.info(f"Data fetched successfully from {path}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching data from {path}: {e}")
        return None

def validate_data(data):
    logging.info("Validating data")
    if not isinstance(data[:1], list):
        logging.error("Data is not a list.")
        return False
    for row in data:
        if row[0] is None:
            logging.error(f"Invalid data found in row: {row}")
            return False
        if row[1] is None:
            logging.error(f"Invalid data found in row: {row}")
            return False
        if row[2] is None or row[2].get('key') is None:
            logging.error(f"Invalid data found in row: {row}")
            return False
    logging.info("Data validation completed successfully.")
    return True

def transform_data(data):
    logging.info("Transforming data")
    transformed_data = []
    for row in data:
        if 'UserId' in row and 'Id' in row and 'Title' in row:
            transformed_data.append({
                'UserId': row['UserId'],
                'Id': row['Id'],
                'Title': row['Title'],
            })
    logging.info("Data transformation completed successfully.")
    return transformed_data

def save_json(data, filename):
    logging.info(f"Saving data to {filename} as JSON")
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    logging.info(f"Data saved to {filename} successfully.")

def save_csv(data, filename):
    logging.info(f"Saving data to {filename} as CSV")
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    logging.info(f"Data saved to {filename} successfully.")

path = "https://dummyjson.com/"

data = fetch_data(path)
if data is not None:
    if validate_data(data):
        transformed_data = transform_data(data)
        save_json(transformed_data, "output.json")
        save_csv(transformed_data, "output.csv")