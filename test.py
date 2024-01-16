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
import ee

ee.Authenticate()

ee.Initialize(project='tuproq')

if __name__ == '__main__':
    pass
