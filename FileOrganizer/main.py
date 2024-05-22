import os
import shutil
from pathlib import Path

# file types and their extensions
folder_names = {
  "Compressed":{'7z','deb','pkg','rar','rpm', 'tar.gz','z', 'zip'},
  'Code':{'js','jsp','html','ipynb','py','java','css', 'json'},
  'Documents':{'ppt','pptx','pdf','xls', 'xlsx','doc','docx','txt', 'tex', 'epub'},
  'Images':{'bmp','gif .ico','jpeg','jpg','png','jfif','svg','tif','tiff'},
  'Softwares':{'apk','bat','bin', 'exe','jar','msi','py'},
  'Videos':{'3gp','avi','flv','h264','mkv','mov','mp4','mpg','mpeg','wmv'},
  'Others': {None}
}

download_path = r"/Users/hwoodie/Downloads"

# find files (not including .localized and .DNS_Store)
files = [f for f in os.listdir(download_path) if os.path.isfile(os.path.join(download_path, f)) and (f != '.localized' and f != '.DS_Store')]
# print(files)

# create folders if they don't exist
for folder in folder_names.keys():
  Path(os.path.join(download_path, folder)).mkdir(exist_ok=True)

extension_filetype_map = {extension: fileType 
        for fileType, extensions in folder_names.items() 
                for extension in extensions }

def new_path(file):
  extension = str(file).split('.')[-1]
  # print(extension)
  amplified_folder = extension_filetype_map[extension] if extension in extension_filetype_map.keys() else 'Others'
  final_path = os.path.join(download_path,amplified_folder)
  # print(final_path)
  return final_path

for eachfile in files:
  shutil.move(os.path.join(download_path,eachfile), new_path(eachfile))