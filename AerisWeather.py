import requests
import threading
import json
import isodate
import csv
from datetime import datetime, timezone
import glob
import csv
import pandas as pd


def init():
    print("Init AerisWeather")
    global timer
    GetData()
    #threading.Timer(60*30, GetData).start()


def GetData():
    threading.Timer(60, GetData).start()
    #if not datetime.now().minute == 1:
    if  datetime.now().minute == 1 and datetime.now().hour > 3 and datetime.now().hour < 19:
        print("Getting data")
        try:
            response = requests.get(
                'https://api.aerisapi.com/forecasts/47.549761,33.911244?format=json&filter=detailed,1h&limit=3&client_id=yWayoowrZV34CDtcUOhGs&client_secret=RvOzY5qO29V29wkbltJpSRSRn4uwsP1nqF3xBbU8')
            data = json.loads(response.text)
            forecast_data = data["response"][0]["periods"][2]
            forecast_data['timestamp'] = forecast_data['timestamp'] + 10800
            forecast_data['dt_string'] = datetime.utcfromtimestamp(forecast_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            print(forecast_data)

            WriteNewLinesToFile(forecast_data)

        except Exception as e:
            print("Error during getting data from opendata")
            print(e)


def WriteNewLinesToFile(forecast_data):
    print("Writing to file")
    with open('data/forecasted_data_AerisWeather.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([forecast_data["timestamp"],forecast_data["dt_string"],forecast_data["avgTempC"],forecast_data["sky"],forecast_data["visibilityKM"],forecast_data["solradWM2"]])















init()