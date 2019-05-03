# Purpose: bag and validate each aip folder.
# Dependencies: bagit.py

import os
import shutil
import subprocess
from variables import *


print('\n>>>Packaging AIPs...\n')

# Delete any .DS_Store or Thumbs.db because they cause errors with bag validation.
for root, dirs, files in os.walk('.'):
  for item in files:
    if item == '.DS_Store' or item == 'Thumbs.db':
      os.remove(f'{root}/{item}')
	  
	  
# Bag the AIPs and validate the bags.
bag_count = 0
total = len(os.listdir(aips_directory))

for item in os.listdir(): 
  # Displays a progress count because this step can take a long time.
  bag_count += 1
  print(f'Bagging AIP {bag_count} of {total}.')	 

  subprocess.run(f'bagit.py --quiet --md5 {item}', shell=True)
  os.replace(item, f'{item}_bag')

  # If the bag does not validate, move to an error folder.
  validation_result = subprocess.run(f'bagit.py --validate --quiet {item}_bag', stderr=subprocess.PIPE, shell=True)
  if 'invalid' in str(validation_result):
    move_error('bag_invalid', f'{item}_bag')
