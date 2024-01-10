import glob
import csv




def init():
    print(GetFiles())
    forecast_data = GetForecastData()
    data_to_analize = []
    for file_name in GetFiles():
        actual_production_lines = GetDataFromHuaweiFile(file_name)
        for actual_production_line in actual_production_lines:
            for forecast_data_line in forecast_data:
                if actual_production_line[0] == forecast_data_line[9]:
                    print("Founded - ",actual_production_line[0],forecast_data_line[9])
                    data_to_analize_line = forecast_data_line + [actual_production_line[1]]
                    data_to_analize.append(data_to_analize_line)
                    #print(data_to_analize_line)
    WriteDataToAnalizeToCSV(data_to_analize)
    CheckHeaders()

def GetFiles():
    file_names = []
    for file_name in glob.glob("files/*.csv"):
        file_names.append(file_name)
    return file_names

def ReadFile(file_name):
    array = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            array.append(row)
    f.close()
    for row in array:
        print(row[0],row[1])
    #print(len(array))

def GetDataFromHuaweiFile(file_name):
    file_text = ''
    with open(file_name, 'r',encoding="utf16", errors='ignore') as f:
        file_text = f.read()
    f.close()
    rows = file_text.splitlines()
    rows.pop(1)
    rows.pop(0)
    stripped_rows = []
    for row in rows:
        stripped_row = "".join(row.split())
        stripped_row = stripped_row.replace('""',',')
        stripped_row = stripped_row[1:]
        stripped_row = stripped_row.replace('"',',')
        cols = stripped_row.split(',')
        stripped_row = cols[0] + "," + cols[1]
        cols[0] = cols[0][:10] + " " + cols[0][10:]
        stripped_rows.append(cols)
        #print(row)
   # for stripped_row in stripped_rows:
       # print(stripped_row)
    return stripped_rows


def GetForecastData():
    array = []
    with open("data/forecasted_data.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            #print(row)
            array.append(row)
    f.close()
    array.pop(0)
    return array


def WriteDataToAnalizeToCSV(data):
    with open('data_for_analyze/clear_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for newLine in data:
            writer.writerow([newLine[0],newLine[1],newLine[2],newLine[3],newLine[4],newLine[5],newLine[6],newLine[7],newLine[8],newLine[9],newLine[10]])
    file.close()


def CheckHeaders():
    with open('data_for_analyze/clear_data.csv', 'r') as f:
        text = f.read()
    f.close()
    if not text[:3] == "ghi":
        new_text = "ghi,ebh,dni,dhi,air_temp,zenith,azimuth,cloud_opacity,timestamp,datetime,actual_power\n" + text
        with open('data_for_analyze/clear_data.csv', 'w') as f2:
            f2.write(new_text)
        f2.close()


init()