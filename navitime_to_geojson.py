import requests
import os
import pandas as pd
import geojson
from mapboxgl.utils import df_to_geojson
from flask import Flask
from flask import render_template

mapbox_token = 'pk.eyJ1Ijoia291dGEwNDIyIiwiYSI6ImNrdGJxcHRseDF5czYyb3FraWU5Znp3cTkifQ.cknW15ccrf7NCR4bQtlUkA'
rapidapi_key = 'c38f754eeamshe5c7f581381f479p1a4cb4jsn7e2d577d20e8'

app = Flask(__name__)

headers = {
        'x-rapidapi-host': "navitime-reachable.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
        }

tsudanuma_loc = "35.691276738069,140.02032888852"

def flatten(d, parent_key='', sep='_'):
        """
        flatten dictionary
        https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
        """
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

@app.route("/")
def show_transit():
    points = transit()
    return render_template('transit.html', points=points)

@app.route("/walk")
def show_walk():
    points = walk()
    return render_template('walk.html', points = points)

@app.route("/car")
def show_car():
    points = car()
    return render_template('car.html', points = points)

def transit():
    from collections import MutableMapping
    def flatten(d, parent_key='', sep='_'):
        """
        flatten dictionary
        https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
        """
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    url = "https://navitime-reachable.p.rapidapi.com/reachable_transit"
    querystring = {
        "start":tsudanuma_loc,
        "term":"180",
        "term_from":"0",
        "walk_speed":"5",
        "transit_limit":"30",
        "offset":"0",
        "limit":"2000",
        "datum":"wgs84",
        "coord_unit":"degree",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    tsudanuma = response.json()
    items = [flatten(item) for item in tsudanuma['items']]
    df = pd.DataFrame(items)
    points = df_to_geojson(df,
                        properties=['name', 'node_id', 'time', 'transit_count'],
                        lat='coord_lat',
                        lon='coord_lon',
                        precision=6)
    #ファイル出力
    # if(os.path.exists('navitime_reachable_transit.geojson')):
    #     os.remove('navitime_reachable_transit.geojson')
    #     with open("navitime_reachable_transit.geojson", 'w') as outfile:
    #      geojson.dump(points, outfile)
    # else:
    #     with open("navitime_reachable_transit.geojson", 'w') as outfile:
    #      geojson.dump(points, outfile)
    print(type(points))

    return points

def walk():
    from collections import MutableMapping
    def flatten(d, parent_key='', sep='_'):
        """
        flatten dictionary
        https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
        """
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    url = "https://navitime-reachable.p.rapidapi.com/reachable_walk"
    terms = [30,60,180]
    tsudanuma = {'key1':'','key2':'','key3':''}
    i = 0
    for key in tsudanuma.keys():
        querystring = {"start":tsudanuma_loc,"datum":"wgs84","term":terms[i],"coord_unit":"degree"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        tsudanuma[key] = response.json()
        i = i+1


    item1 = [flatten(item) for item in tsudanuma['key1']['items']]
    item2 = [flatten(item) for item in tsudanuma['key2']['items']]
    item3 = [flatten(item) for item in tsudanuma['key3']['items']]
    items = item1 + item2 + item3
    df = pd.DataFrame(items)
    points = df_to_geojson(df,
                        properties=['time'],
                        lat='coord_lat',
                        lon='coord_lon',
                        precision=6)

    return points

def car():
    from collections import MutableMapping
    def flatten(d, parent_key='', sep='_'):
        """
        flatten dictionary
        https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
        """
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    url = "https://navitime-reachable.p.rapidapi.com/reachable_car"
    terms = [30,60,180]
    tsudanuma = {'key1':'','key2':'','key3':''}
    i = 0
    for key in tsudanuma.keys():
        querystring = {"start":tsudanuma_loc,"datum":"wgs84","term":terms[i],"car_fare":"toll","coord_unit":"degree"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        tsudanuma[key] = response.json()
        i = i+1


    item1 = [flatten(item) for item in tsudanuma['key1']['items']]
    item2 = [flatten(item) for item in tsudanuma['key2']['items']]
    item3 = [flatten(item) for item in tsudanuma['key3']['items']]
    items = item1 + item2 + item3
    df = pd.DataFrame(items)
    points = df_to_geojson(df,
                        properties=['time'],
                        lat='coord_lat',
                        lon='coord_lon',
                        precision=6)

    return points