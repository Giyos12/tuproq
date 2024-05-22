# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# import io
# import os
#
#
# def main():
#     # Load the service account credentials
#     creds = Credentials.from_service_account_file('able-handbook-393809-e8f98af11465.json')
#
#     # Build the drive service
#     drive_service = build('drive', 'v3', credentials=creds)
#
#     # Define the folder ID
#     folder_id = '17wd30R2YHt7b7tPwrcgvUB3WeEiHqs0c'  # replace 'folder_id' with the ID of the folder
#
#     # Call the files().list() method to list the files in the folder
#     results = drive_service.files().list(
#         q="'{}' in parents".format(folder_id),
#         fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#
#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print('{0} ({1})'.format(item['name'], item['id']))
#
#             # Call the files().get_media() method to download the file
#             request = drive_service.files().get_media(fileId=item['id'])
#
#             fh = io.BytesIO()
#             downloader = MediaIoBaseDownload(fh, request)
#             done = False
#             while done is False:
#                 status, done = downloader.next_chunk()
#                 print("Download %d%%." % int(status.progress() * 100))
#
#             # Write the file to disk
#             with open(os.path.join('.', item['name']),
#                       'wb') as f:  # replace 'download_folder' with the path to the folder where you want to download the files
#                 f.write(fh.getvalue())
#
#
# if __name__ == '__main__':
#     main()
#
# import ee
#
# service_account = 'tuproq@tuproq.iam.gserviceaccount.com'
# credentials = ee.ServiceAccountCredentials(service_account, 'tuproq-bb60103973b6.json')
# ee.Initialize(credentials)
import csv
import json

import ee

service_account = 'tuproq@tuproq.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'tuproq-bb60103973b6.json')
ee.Initialize(credentials)

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


if __name__ == '__main__':
    write_csv_file('2024-03-01', '2024-04-7')
