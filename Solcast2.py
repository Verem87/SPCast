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
    print("Init SolCast")
    global timer
    GetData()
    #threading.Timer(60*30, GetData).start()


def GetData():
    threading.Timer(60, GetData).start()
    forecast_data = {}
    #if not datetime.now().minute == 1:
    if datetime.now().minute == 1 and datetime.now().hour > 3 and datetime.now().hour < 19:

        print("Getting data")
        try:
            response = requests.get(
                'https://api.solcast.com.au/world_radiation/forecasts?format=json&api_key=32YBXPSc6gufUvbE9JKTBLRZ7w_6Lb0i&latitude=47.549761&longitude=33.911244')
            data = json.loads(response.text)
            forecast_data = data["forecasts"][6]
            forecast_data2 = data["forecasts"][7]

            utc_dt = isodate.parse_datetime(forecast_data["period_end"])
            local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
            forecast_data["timestamp"] = int(datetime.timestamp(local_dt))


            forecast_data['dt'] = forecast_data['timestamp'] + 9000
            forecast_data['dt_string'] = datetime.utcfromtimestamp(forecast_data['dt']).strftime('%Y-%m-%d %H:%M:%S')

            forecast_data["ghi"] = (forecast_data["ghi"]+forecast_data2["ghi"])/2
            forecast_data["ebh"] = (forecast_data["ebh"]+forecast_data2["ebh"])/2
            forecast_data["dni"] = (forecast_data["dni"]+forecast_data2["dni"])/2
            forecast_data["dhi"] = (forecast_data["dhi"]+forecast_data2["dhi"])/2
            forecast_data["air_temp"] = (forecast_data["air_temp"]+forecast_data2["air_temp"])/2
            forecast_data["cloud_opacity"] = (forecast_data["cloud_opacity"]+forecast_data2["cloud_opacity"])/2
            print(forecast_data["cloud_opacity"],forecast_data2["cloud_opacity"])
            print(forecast_data)

            WriteNewLinesToFile(forecast_data)

        except Exception as e:
            print("Error during getting data from SolCast")
            print(e)


def WriteNewLinesToFile(forecast_data):
    print("Writing to file")
    with open('data/forecasted_data_SolCast.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([forecast_data["dt"], forecast_data["dt_string"], forecast_data["ghi"], forecast_data["ebh"], forecast_data["dni"], forecast_data["dhi"], forecast_data["air_temp"], forecast_data["cloud_opacity"]])



init()