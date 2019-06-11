# Purpose: make md5manifest of zipped bags and move to ingest server.
# Dependencies: md5deep, rsync 

import datetime
import os
import shutil
import subprocess
from variables import *


print('\n>>>Making MD5 manifest and moving AIPs to ingest server...\n')

os.chdir(f'{aip_staging}/aips-ready-to-ingest')

# Set a date variable equal to current date.
date = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

#Make MD5 manifest of all packaged AIPs (bagged, tarred, and zipped).
subprocess.run(f'md5deep -br {os.getcwd()} > {aip_staging}/md5-manifests-for-aips/{date}_AIPs_md5_manifest.txt', shell=True)

#Copy to ingest server.
for item in os.listdir():
  
  #Using a for loop with rsync instead of the -r (recursive) option
  #so can identify which file, if any, has an error rather than failing the whole batch for any error.
  rsync_result = subprocess.run(f'rsync -v --progress {item} {ingest_server}', stderr=subprocess.PIPE, shell=True)

  #If copied correctly, move to a different folder on AIPs staging. Otherwise, move to an error folder.
  if "stderr=b''" in str(rsync_result):
    shutil.move(item, f'{aip_staging}/aips-already-on-ingest-server/{item}')
  else:    
    move_error('copy_to_ingest_failed', item)
