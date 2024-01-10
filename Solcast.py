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
    print("Init solcast")
    global timer
    GetData()
    threading.Timer(60*30, GetData).start()


def GetData():
    print("Getting data")
    threading.Timer(3600*2, GetData).start()
    forecast_data = {}
    try:
        response = requests.get('https://api.solcast.com.au/weather_sites/286d-45eb-5d4c-5f8a/forecasts?format=json&api_key=kQfta_yG6YgIX40PGhCodENA9wLp4Hg6')
        data = json.loads(response.text)["forecasts"]
        for row in data:
            utc_dt = isodate.parse_datetime(row["period_end"])
            local_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
            row["timestamp"] = int(datetime.timestamp(local_dt))
            row["datetime"] = local_dt.strftime("%Y-%m-%d %H:%M:%S")
            row["azimuth"] = abs(row["azimuth"])
            row.pop("period_end",None)
            row.pop("period",None)
            row.pop("period",None)
            #print(row)
        data.sort(key=lambda r: r["timestamp"])
        data = data[:144]
        forecast_data = ExtrapolateData(data)
    except Exception as e:
        print("Error during getting data from solcast")
        print(e)
    #data_from_file = CheckAvailableDataFiles()
    #print(type(forecast_data),type(forecast_data[0]),forecast_data[0],data_from_file[0])
    FindNewForcastedLines(forecast_data)
    #for data_row_in_forecast in forecast_data:
   #     for data_row_in_actual_data in data_from_file:
   #         if data_row_in_forecast["datetime"] == data_row_in_actual_data[0]:
   #             print("Founded")
   #             data_row_in_forecast["actual_power"] = data_row_in_actual_data[2]

def GetDataFromFile():
    array = []
    with open("data/forecasted_data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            #print(row)
            array.append(row)
    f.close()
    return array

def FindNewForcastedLines(ForcastedData):
    newLines = []
    SavedData = GetDataFromFile()
    print('saved data len - ',len(SavedData))
    k = 0
    if SavedData == []:
        WriteNewLinesToFile(ForcastedData)
        return
    for i in range(0,len(ForcastedData)):
        for j in range(0,len(SavedData)):
            if ForcastedData[i]["datetime"] == SavedData[j][9]:
                SavedData[j][0] = ForcastedData[i]["ghi"]
                SavedData[j][1] = ForcastedData[i]["ebh"]
                SavedData[j][2] = ForcastedData[i]["dni"]
                SavedData[j][3] = ForcastedData[i]["dhi"]
                SavedData[j][4] = ForcastedData[i]["air_temp"]
                SavedData[j][5] = ForcastedData[i]["zenith"]
                SavedData[j][6] = ForcastedData[i]["azimuth"]
                SavedData[j][7] = ForcastedData[i]["cloud_opacity"]
                k = k+1
                break
            if j == (len(SavedData)-1):
                newLines.append(MakeDataRowFromDict(ForcastedData[i]))
    if len(newLines)>0:
        for newLine in newLines:
            SavedData.append(newLine)
        print('new saved data len - ', len(SavedData))
        UpdateFile(SavedData)
    else:
        print('no additional data')

def WriteNewLinesToFile(newLines):
    print(newLines)
    with open('data/forecasted_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for newLine in newLines:
            writer.writerow([newLine["ghi"],newLine["ebh"],newLine["dni"],newLine["dhi"],newLine["air_temp"],newLine["zenith"],newLine["azimuth"],newLine["cloud_opacity"],newLine["timestamp"],newLine["datetime"]])

def UpdateFile(data):
    with open('data/forecasted_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def MakeDataRowFromDict(newLine):
    row = [newLine["ghi"],newLine["ebh"],newLine["dni"],newLine["dhi"],newLine["air_temp"],newLine["zenith"],newLine["azimuth"],newLine["cloud_opacity"],newLine["timestamp"],newLine["datetime"]]
    return row


def ExtrapolateData(data):
    print("Extrapolating ... ")
    extrapolated_data = data.copy()
    print("len before - ",len(data))
    for i in range(1, len(data)):
        prev_row = data[i-1]
        row = data[i]
        for j in range(1,6):
            new_row = prev_row.copy()
            for key in row:
                if key != "datetime":
                    delta = float(row[key]) - float(prev_row[key])
                    new_row[key] = round(prev_row[key] + delta*j/6)
                    #if key == "timestamp":
                        #print(row[key],prev_row[key],new_row[key],delta,j,delta*j/6)
            new_row["datetime"] = datetime.utcfromtimestamp(new_row["timestamp"]+3*60*60).strftime('%Y-%m-%d %H:%M:%S')

            """SWITCH TO LOCAL TIME!!!"""
            extrapolated_data.append(new_row)
    #print(len(extrapolated_data))


    extrapolated_data.sort(key=lambda r: r["timestamp"])
    print("len after - ",len(extrapolated_data))

    #for i in range(0, len(extrapolated_data)):
        #print(extrapolated_data[i])
    return extrapolated_data


def CheckAvailableDataFiles():
    array = []
    for file_name in glob.glob("files/*.csv"):
        with open(file_name, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                array.append(row)
        f.close()
    return array


init()