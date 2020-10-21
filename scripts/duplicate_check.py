# Purpose: test if an AIP has already been made so don't duplicate effort.
# Dependencies: none

import os
import pathlib
from variables import *


print('\n>>>Checking for duplication...\n')

for item in os.listdir():
  # Calculates aip_id from the file name.
  aip_id = ''

  if workflow == 'dpx':
    if item.startswith('har'):
      aip_id = item
    else:
      aip_id = f'bmac_{item}'

  if workflow == 'mkv' or workflow == 'mov' or workflow == 'mkv-filmscan' or workflow == 'wav':
    aip_id = f'bmac_{pathlib.Path(item).stem}'

  if workflow == 'mxf':
    aip_id = f'bmac_wsb-video_{pathlib.Path(item).stem}'.lower()

  # Creates a list of all files in the three places that finished aips are stored locally.
  ready = os.listdir(f'{aip_staging}/aips-ready-to-ingest')
  already = os.listdir(f'{aip_staging}/aips-already-on-ingest-server')
  ingest = os.listdir(ingest_server)
  dedup_list = ready + already + ingest

  # If an AIP about to be processed has the same aip_id as a finished aip, moves to an error folder.
  # Not testing for an exact match to the finished aip since that filename includes the file size after processing.
  for zip in dedup_list:
    if zip.startswith(aip_id):
      move_error('duplicate_aip', item)
      #Moves associated MD5 files for the AIP to the error folder as well.
      if workflow == 'mkv' or workflow == 'mov' or workflow == 'wav':
        move_error('duplicate_aip', f'{item}.md5')
