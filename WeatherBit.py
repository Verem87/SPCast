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
    print("Init WeatherBit")
    global timer
    GetData()
    #threading.Timer(60*30, GetData).start()


def GetData():
    threading.Timer(60, GetData).start()
    #if not datetime.now().minute == 1:
    if  datetime.now().minute == 1 and datetime.now().hour > 3 and datetime.now().hour < 19:
        print("Getting data")
        try:
            PARAMS = {'apikey': 'I5Z5fGppFX66hGm1UaK272tI9nPos39R','language':'en-us','details': 'true', 'metric': 'true'}
            response = requests.get(
                'http://api.weatherbit.io/v2.0/forecast/hourly?key=32a26900cff04126a5da2cdbcffeb795&lang=en&units=M&hours=3&lat=47.549761&lon=33.911244')
            data = json.loads(response.text)
            forecast_data = data['data'][2]
            forecast_data['ts'] = forecast_data['ts'] + 10800
            forecast_data['dt_string'] = datetime.utcfromtimestamp(forecast_data['ts']).strftime('%Y-%m-%d %H:%M:%S')
            print(forecast_data)

            WriteNewLinesToFile(forecast_data)

        except Exception as e:
            print("Error during getting data from opendata")
            print(e)


def WriteNewLinesToFile(forecast_data):
    print("Writing to file")
    with open('data/forecasted_data_WeatherBit.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([forecast_data["ts"],forecast_data["dt_string"],forecast_data["temp"],forecast_data["clouds"],forecast_data["clouds_low"],forecast_data["clouds_mid"],forecast_data["clouds_hi"],forecast_data["solar_rad"],forecast_data["dni"],forecast_data["dhi"],forecast_data["ghi"],forecast_data["vis"]])





















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