from stations import station
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

    return MongoClient("mongodb+srv://" + user + ":" + password + "@" + url + "/?retryWrites=true&w=majority")['Self-Services-Bicycle']

def get_vlille():
    url = 'https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&lang=fr&rows=1000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    data_list = response_json.get('records', [])
    stations = []
    for data in data_list :
        current_station = {
            'recordid' : 'Lille-' + data['recordid'],
            'pos' : data['fields']['geo'],
            'name' : data['fields']['nom'],
            'size' : data['fields']['nbplacesdispo'] + data['fields']['nbvelosdispo'],
            'available' : True if data['fields']['etat'] == 'EN SERVICE' else False,
            'tpe' : True if data['fields']['type'] == 'AVEC TPE' else False
        }
        stations.append(current_station)
    return stations

def get_velov():
    url = 'https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json?maxfeatures=-1&start=1'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    data_list = response_json.get('values', [])
    stations = []
    for data in data_list :
        current_station = {
            'recordid' : 'Lyon-' + str(data['gid']),
            'pos' : [data['lat'], data['lon']],
            'name' : data['name'],
            'size' : data['bike_stands'],
            'available' : True if data['availabilitycode'] == 1 else False,
            'tpe' : True if data['banking'] == 'true' else False
        }
        stations.append(current_station)
    return stations

def get_vlib():
    url = 'https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1000&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    data_list = response_json.get('records', [])
    stations = []
    for data in data_list :
        current_station = {
            'recordid' : 'Paris-' + data['recordid'],
            'pos' : data['fields']['coordonnees_geo'],
            'name' : data['fields']['name'],
            'size' : data['fields']['capacity'],
            'available' : True if data['fields']['is_installed'] == 'OUI' else False,
            'tpe' : True if data['fields']['is_renting'] == 'OUI' else False
        }
        stations.append(current_station)
    return stations

def get_velostar():
    url = 'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=1000&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles'
    response = requests.request('GET', url)
    response_json = json.loads(response.text.encode('utf8'))
    data_list = response_json.get('records', [])
    stations = []
    for data in data_list :
        current_station = {
            'recordid' : 'Rennes-' + data['recordid'],
            'pos' : data['fields']['coordonnees'],
            'name' : data['fields']['nom'],
            'size' : data['fields']['nombreemplacementsactuels'],
            'available' : True if data['fields']['etat'] == 'En fonctionnement' else False,
            'tpe' : True if data['fields']['etat'] == 'En fonctionnement' else False
        }
        stations.append(current_station)
    return stations


def main():
    db = connectDB()
    data = get_vlille() + get_vlib() + get_velov() + get_velostar()
    db.stations.drop()
    db.stations.insert_many(data)
    db.stations.create_index([('pos','2dsphere')])

if __name__ == "__main__":
    main()