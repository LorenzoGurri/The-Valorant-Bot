# MongoDB stuff
import pymongo
from pymongo import MongoClient

# env stuff
import os
from dotenv import load_dotenv
import csv

# Loads the .env file that resides on the same level as the script.
load_dotenv()

# get the Databases
CONNECTION_URL = os.getenv("DB_CONNECTION", "knf")
if CONNECTION_URL == "knf":
    print("Error: Key not found!")
    exit(1)
cluster = MongoClient(CONNECTION_URL)

db = cluster["ValorantBot"]
collection = db["Lineups"]

header = ["Video", "Map", "Site", "Type", "Start", "Agent"]

# Start adding stuff to DB
csvfile = open("lineups/test.csv", "r")
reader = csv.DictReader(csvfile)
for each in reader:
    row = {}
    for field in header:
        row[field] = each[field]
    print("ROW: ", row)
    collection.insert_one(row)
