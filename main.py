from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


def connectDB():
    url = os.environ.get('databaseUrl')
    user = os.environ.get('databaseUser')
    password = os.environ.get('databaseKey')

    return MongoClient("mongodb+srv://" + user + ":" + password + "@" + url + "/?retryWrites=true&w=majority")

def main():
    db = connectDB()

if __name__ == "__main__":
    main()