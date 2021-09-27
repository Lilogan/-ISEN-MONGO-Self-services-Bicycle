from pymongo import MongoClient
from dotenv import load_dotenv
import time
import os
import requests
import json
from live_data import live_data

load_dotenv()

def connectDB():
    url = os.environ.get('databaseUrl')
    user = os.environ.get('databaseUser')
    password = os.environ.get('databaseKey')

    return MongoClient("mongodb+srv://" + user + ":" + password + "@" + url + "/?retryWrites=true&w=majority")["Self-Services-Bicycle"]

def get_vlille(db):
    url = 'https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&lang=fr&rows=1000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    response_array = response_json.get('records', [])
    data = []
    for vlille_data in response_array:
        data.append(live_data("Lille-"+vlille_data["recordid"], vlille_data["fields"]["nom"], vlille_data["fields"]["nbvelosdispo"],vlille_data["fields"]["nbplacesdispo"]).__dict__)
    return data

def get_velov(db):
    url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=-1&start=1'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    response_array = response_json.get('values', [])
    data = []
    for velov_data in response_array:
        data.append(live_data("Lyon-"+str(velov_data["gid"]), velov_data["name"], velov_data["available_bikes"],velov_data["available_bike_stands"]).__dict__)
    return data

def get_vlib(db):
    url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1000&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    response_array = response_json.get('records', [])
    data = []
    for vlib_data in response_array:
        data.append(live_data("Paris-"+vlib_data["recordid"], vlib_data["fields"]["name"], vlib_data["fields"]["numbikesavailable"],vlib_data["fields"]["capacity"]-vlib_data["fields"]["numbikesavailable"]).__dict__)
    return data

def get_velostar(db):
    url = 'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=1000&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    response_array = response_json.get('records', [])
    data = []
    for velostar_data in response_array:
        data.append(live_data("Rennes-"+velostar_data["recordid"], velostar_data["fields"]["nom"], velostar_data["fields"]["nombrevelosdisponibles"],velostar_data["fields"]["nombreemplacementsactuels"]).__dict__)
    return data

    
def main():
    db = connectDB()
    while True:
        data = get_vlille(db)
        data += get_velov(db)
        data += get_vlib(db)
        data += get_velostar(db)
        db["history"].insert_many(data)
        time.sleep(60)

if __name__ == "__main__":
    main()