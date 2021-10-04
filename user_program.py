from pymongo import MongoClient
from dotenv import load_dotenv
import time
import os
import requests
import json
from live_data import live_data
from bson.son import SON


load_dotenv()

def connectDB():
    url = os.environ.get('databaseUrl')
    user = os.environ.get('databaseUser')
    password = os.environ.get('databaseKey')

    return MongoClient("mongodb+srv://" + user + ":" + password + "@" + url + "/?retryWrites=true&w=majority")["Self-Services-Bicycle"]

def main():
    db = connectDB()
    latitude = input("Latitude: ")
    longitude = input("Longitude: ")
    res = db["stations"].find({"pos": SON({"$near": { "$geometry": {"type": "Point", "coordinates": [float(latitude), float(longitude)]}}})})
    for a in res:
        print(a)

if __name__ == "__main__":
    main()