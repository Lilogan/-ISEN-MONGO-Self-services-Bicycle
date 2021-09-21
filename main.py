from pymongo import MongoClient
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


def connectDB():
    url = os.environ.get('databaseUrl')
    user = os.environ.get('databaseUser')
    password = os.environ.get('databaseKey')

    return MongoClient("mongodb+srv://" + user + ":" + password + "@" + url + "/?retryWrites=true&w=majority")

def get_vlille():
    url = 'https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&lang=fr&rows=1000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get('records', [])

def get_velov():
    url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=-1&start=1'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get('values', [])

def get_vlib():
    url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1000&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get('records', [])

def get_velostar():
    url = 'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=1000&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get('records', [])


def main():
    db = connectDB()

if __name__ == "__main__":
    main()