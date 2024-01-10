import requests
import threading
import json
import isodate
import csv
from datetime import datetime, timezone
import glob
import csv
import pandas as pd
import  time

def init():
    print("Init SolarWeb")
    global timer
    GetData()
    #threading.Timer(60*30, GetData).start()


def GetData():
    threading.Timer(60, GetData).start()
    forecast_data = {}
    #if not datetime.now().minute == 1:

    if  datetime.now().minute == 1 and datetime.now().hour > 3 and datetime.now().hour < 19:
        print("Getting data")
        try:
            response = requests.get(
                'https://mdx.meteotest.ch/api_v1?key=08EE2F22AD1B93B0DAA612DD9CCD2859&service=solarforecast&action=getforecast&site_id=563219&format=json')
            data = json.loads(response.text)
            forecast_data_keys = getList(data["payload"]['solarforecast']['563219'])
            #print(forecast_data.keys())
            forecast_data =   data["payload"]['solarforecast']['563219'][str(forecast_data_keys[2])]
           # print(forecast_data, forecast_data_keys[2])

            ts = int(time.mktime(datetime.strptime(forecast_data_keys[2], "%Y-%m-%d %H:%M:%S").timetuple())) + 21600
          #  print(ts)
            forecast_data['dt'] = ts
            forecast_data['dt_string'] = datetime. utcfromtimestamp(forecast_data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            print(forecast_data)

            WriteNewLinesToFile(forecast_data)

        except Exception as e:
            print("Error during getting data from opendata")
            print(e)


def WriteNewLinesToFile(forecast_data):
    print("Writing to file")
    with open('data/forecasted_data_SolarWeb.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([forecast_data["dt"],forecast_data["dt_string"],forecast_data["bh"],forecast_data["dd"],forecast_data["dh"],forecast_data["dni"],forecast_data["e"],forecast_data["ff"],forecast_data["fx"],forecast_data["gh"],forecast_data["gh_max"],forecast_data["gk"],forecast_data["qff"],forecast_data["rh"],forecast_data["rr"],forecast_data["sy"],forecast_data["tcc"],forecast_data["tt"]])


def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list

init()