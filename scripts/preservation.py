# Purpose: create preservation.xml from mediainfo xml.
# Dependencies: saxon, xmllint, xslt stylesheet

import os
import shutil
import subprocess
from variables import *


print('\n>>>Creating preservation.xml files...\n')

for item in os.listdir():
   
  # Run stylesheet on mediainfo xml to create preservation.xml metadata file.
  subprocess.run(f'java -cp {saxon} net.sf.saxon.Transform -s:{item}/metadata/{item}_mediainfo.xml -xsl:{stylesheet} -o:{item}/metadata/{item}_preservation.xml department="{department}"', shell=True)

  # Validate preservation.xml against preservation.xsd.
  validation_result = subprocess.run(f'xmllint --noout -schema {xsd} {item}/metadata/{item}_preservation.xml', stderr=subprocess.PIPE, shell=True)

  # If it isn't valid, move the AIP to an error folder.
  # If it is valid, copies the preservation.xml to local server for staff use.
  if 'failed to load' in str(validation_result) or 'fails to validate' in str(validation_result):
    move_error('preservation_invalid', item)
  else:
    shutil.copy2(f'{item}/metadata/{item}_preservation.xml', f'{aip_staging}/preservation_xmls')
