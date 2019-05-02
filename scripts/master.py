# Purpose: create master.xml from mediainfo xml.
# Dependencies: saxon, xmllint, xslt stylesheet

import os
import shutil
import subprocess
from variables import *


print('\n>>>Creating master.xml files...\n')

for item in os.listdir():
   
  # Run stylesheet on mediainfo xml to create master.xml metadata file.
  subprocess.run(f'java -cp {saxon} net.sf.saxon.Transform -s:{item}/metadata/{item}_mediainfo.xml -xsl:{stylesheet} -o:{item}/metadata/{item}_master.xml department="{department}"', shell=True)

  # Validate master.xml against master.xsd.
  validation_result = subprocess.run(f'xmllint --noout -schema {aip_staging}/master.xsd {item}/metadata/{item}_master.xml', stderr=subprocess.PIPE, shell=True)

  # If it isn't valid, move the AIP to an error folder.
  # If it is valid, copies the master.xml to local server for staff use.
  if 'failed to load' in str(validation_result) or 'fails to validate' in str(validation_result):
    move_error('master_invalid', item)
  else:
    shutil.copy2(f'{item}/metadata/{item}_master.xml', f'{aip_staging}/master_xmls')
