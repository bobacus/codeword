import csv
import json


def load_csv(filename: str):
    with open(filename, newline='') as f:
        return list(csv.reader(f))

def load_json(filename: str):
    with open(filename) as f:
        return json.load(f)
