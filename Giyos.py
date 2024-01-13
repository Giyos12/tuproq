# Deep Learning bashorat uchun
# ------------------------------------------------------------------ #

# import pickle
# from keras.models import load_model
# import numpy as np
#
# preprocessing = pickle.load(open("pre_salt.pkl", 'rb'))
# model = load_model("salt.h5")
#
#
# def bashorat(B1, B2, B3, B4, B5, B6, B7, B10):
#     data = preprocessing.transform([[B1, B2, B3, B4, B5, B6, B7, B10]])
#     pred = np.argmax(np.around(model.predict(data), 2), axis=1) + 1
#     return pred


# bashorat(9089, 9691, 10991, 11383, 16716, 13850, 11708, 43860)

# Bandlarni olish uchun.
# ------------------------------------------------------------------ #

import json
import ee
import csv
from django.utils import timezone

ee.Initialize(project='tuproq')

data = json.load(open('Konturlar.json'))
data = data['features']


def ret_bands(polygon, boshlanish_data, tugash_data):
    imagelist = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterBounds(polygon).filterDate(boshlanish_data,
                                                                                              tugash_data) \
        .select("SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7", "ST_B10")
    rasmlar_soni = imagelist.size().getInfo()
    image_list = imagelist.toList(imagelist.size())
    bands = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(rasmlar_soni):
        image = ee.Image(image_list.get(i))
        means = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=polygon,
            scale=30)
        means = means.getInfo()
        bands[0] += means["SR_B1"] * 0.9
        bands[1] += means["SR_B2"] * 0.9
        bands[2] += means["SR_B3"] * 0.85
        bands[3] += means["SR_B4"] * 0.85
        bands[4] += means["SR_B5"] * 0.9
        bands[5] += means["SR_B6"] * 0.9
        bands[6] += means["SR_B7"] * 0.9
        bands[7] += means["ST_B10"] * 1.1
    for i in range(len(bands)):
        bands[i] = int(bands[i] / rasmlar_soni)
    return bands


def write_csv_file(boshlanish_data, tugash_data):
    with open(f'media_root/csv/{boshlanish_data}.csv', 'w', newline='') as file1:
        writer = csv.writer(file1)
        writer.writerow(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B10", "Kontur_raq"])

        for i in range(len(data)):
            coors = data[i]['geometry']['coordinates']
            aoi = ee.Geometry.Polygon(coors)
            bands = ret_bands(aoi, boshlanish_data, tugash_data)
            writer.writerow([bands[0], bands[1], bands[2], bands[3], bands[4], bands[5], bands[6], bands[7],
                             data[i]['properties']['Kontur_raq']])
            print(i)
    return f'media_root/csv/{boshlanish_data}.csv'


import calendar
from datetime import datetime
import requests


def func():
    time = datetime.now()

    last_day_of_month = calendar.monthrange(time.year - 2, time.month + 11)[1]
    boshlanish_data = f'{time.year - 2}-{time.month + 11}-01'
    formatted_date = datetime.strptime(boshlanish_data, '%Y-%m-%d')
    file_path = write_csv_file(boshlanish_data=f'{time.year - 2}-{time.month + 11}-01',
                               tugash_data=f'{time.year - 2}-{time.month + 11}-{last_day_of_month}')
    name = str(time)
    files = {'file': open(file_path, 'rb')}
    data = {'name': name, 'date': formatted_date}

    response = requests.post(url='http://127.0.0.1:8000/api/modul/b/', files=files, data=data)

    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    func()
