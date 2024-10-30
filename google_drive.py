from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import GoogleDriveFileList


gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDriveFileList(gauth)
driv = GoogleDrive(gauth)
file1 = driv.CreateFile({'title':'Text.txt'})

file1.SetContentString('Hello world')

file1.Upload()


file_list = driv.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file in file_list:
    print(f"{file['title']} ({file['id']})")
