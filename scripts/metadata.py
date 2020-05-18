# Purpose: extract technical metadata.
# Dependencies: mediainfo, ffmpeg

import os
import shutil
import subprocess
from variables import *


print('\n>>>Extracting metadata...\n')

for item in os.listdir():
 
  # Makes mediainfo XML and saves to metadata folder.
  subprocess.run(f'mediainfo -f --Output=XML --Language=raw {item}/objects > {item}/metadata/{item}_mediainfo.xml', shell=True)
    
  # Copies mediainfo XML to local server for staff use.  
  shutil.copy2(f'{item}/metadata/{item}_mediainfo.xml', f'{aip_staging}/mediainfo-xmls/mediainfo-raw-output')

  # Makes pbcore xml and saves to local server.  
  subprocess.run(f'mediainfo -f --Output=PBCore2 --Language=raw {item}/objects > {aip_staging}/mediainfo-xmls/pbcore2-xml/{item}_mediainfo-pbcore2.xml', shell=True)
     
  # For mxf, makes framemd5 and saves to metadata folder.
  if workflow == 'mxf':
    subprocess.run(f'ffmpeg -loglevel error -i {item}/objects/{item}.mxf -f framemd5 {item}/metadata/{item}.framemd5', shell=True)
	
