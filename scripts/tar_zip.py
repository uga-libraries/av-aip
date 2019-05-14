# Purpose: if MKV, tar ONLY each aip folder. All others: tar and zip each aip folder.
# Dependencies: prepare_bag perl script, prepare_bag_nozip perl script

import os
import shutil
import subprocess
from variables import *

# Recalculating total in case any aips were invalid and moved.
total = len(os.listdir(aips_directory))
tarzip_count = 0


if workflow == 'mkv':
  # Tar the aips using a Perl script.
  # Separate loop so won't get an error if any files are moved due to errors.
  for item in os.listdir():
  # Displays a progress count because this step can take a long time.
    tarzip_count += 1
    print(f'Tar/zipping AIP {tarzip_count} of {total}.')
    subprocess.run(f'perl {prepare_bag_nozip} {item} {aip_staging}/aips-ready-to-ingest/', shell=True)
      
else:
  # Tar and zip the aips using a Perl script.
  # Separate loop so won't get an error if any files are moved due to errors.
  for item in os.listdir():
  # Displays a progress count because this step can take a long time.
    tarzip_count += 1
    print(f'Tar/zipping AIP {tarzip_count} of {total}.')
    subprocess.run(f'perl {prepare_bag} {item} {aip_staging}/aips-ready-to-ingest/', shell=True)
