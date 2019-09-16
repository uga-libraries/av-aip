# Purpose: make aip directory structure and move content to appropriate subdirectories.
# Dependencies: none

import os
import pathlib
import shutil
from variables import *

os.chdir(aips_directory)

print('\n>>>Constructing AIP directories...\n')

for item in os.listdir():

  # Calculates aip_id (and unique_id for dpx, which is aip_id without bmac_) from the file name.
  aip_id = ''
  unique_id = ''

  if workflow == 'dpx':
    unique_id = item

    if item.startswith('har'):
      aip_id = item
    else:
      aip_id = f'bmac_{item}'

  if workflow == 'mkv' or workflow == 'mov' or workflow == 'mkv-filmscan' or workflow == 'wav':
    file_name = os.path.basename(item)
    index_of_dot = file_name.index('.')
    file_name_without_extension = file_name[:index_of_dot]
    aip_id = f'bmac_{file_name_without_extension}'

  if workflow == 'mxf':
    aip_id = f'bmac_wsb-video_{pathlib.Path(item).stem}'.lower()


  # Creates AIP directory structure (folder named aip_id with subfolders objects and metadata).
  if not os.path.exists(aip_id):
    os.mkdir(aip_id)
    os.makedirs(f'{aip_id}/objects')
    os.makedirs(f'{aip_id}/metadata')


  # Rest of this script moves files into the correct subdirectory, renaming if needed.
  # Testing for workflow first is not generally necessary (only .mov is in 2 workflows) but primarily serves to keep the tests organized.

  # DPX files are already in bags, so have to navigate to the data folder to find the content to move into the AIP directory.
  if workflow == 'dpx':
    for root, dirs, files in os.walk(item):
      if root == f'{unique_id}/data':
        for folder in dirs:
          os.replace(f'{root}/{folder}', f'{aip_id}/objects/{folder}-dpx')
        for file in files:
          if file.endswith('.cue'):
            os.replace(f'{root}/{file}', f'{aip_id}/objects/{file}')
          if file.endswith('.mov'):
            shutil.copy2(f'{root}/{file}', f'{aip_staging}/movs-to-bag')
            os.replace(f'{root}/{file}', f'{aip_id}/objects/{file}')
          if file.endswith('.wav'):
            os.replace(f'{root}/{file}', f'{aip_id}/objects/{pathlib.Path(file).stem}-dpx.wav')
    #deletes the original folder after moving all the preservation files into the AIP directory.
    shutil.rmtree(item)

  if workflow == 'mkv' or workflow == 'mov' or workflow == 'mkv-filmscan' or workflow == 'wav':
    if item.endswith('.mkv') or item.endswith('.mov') or item.endswith('.wav'):
      os.replace(item, f'{aip_id}/objects/bmac_{item}')

    if item.endswith('.qctools.xml.gz'):
      os.replace(item, f'{aip_id}/metadata/bmac_{item}')

    if item.endswith('.framemd5'):
      os.replace(item, f'{aip_id}/metadata/bmac_{item}')
	  
  if workflow == 'mxf':
    if item.endswith('.mxf'):
      os.replace(item, f'{aip_id}/objects/bmac_wsb-video_{item.lower()}')
