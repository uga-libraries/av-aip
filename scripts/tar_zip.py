# Purpose: if MKV, tar ONLY each aip folder. All others: tar and zip each aip folder.
# Dependencies: prepare_bag perl script, prepare_bag_nozip perl script
import bz2
import os
import re
import shutil
import subprocess
import tarfile
from variables import *

# Recalculating total in case any aips were invalid and moved.
total = len(os.listdir(aips_directory))
tarzip_count = 0

# Delete any temp files (starts with ".", including .DS_Store) or Thumbs.db that have appeared since last step
for root, dirs, files in os.walk('.'):
  for item in files:
    if item.startswith('.') or item == 'Thumbs.db':
      os.remove(f'{root}/{item}')


if workflow == 'mkv' or workflow == 'mkv-filmscan':
  # Tar the aips using a Perl script.
  # Separate loop so won't get an error if any files are moved due to errors.
  for item in os.listdir():
  # Displays a progress count because this step can take a long time.
    tarzip_count += 1
    print(f'Tarring AIP {tarzip_count} of {total}.')
    subprocess.run(f'perl {prepare_bag_nozip} {item} {aip_staging}/aips-ready-to-ingest/', shell=True)
      
else:
  # Tar and zip the aips using a Perl script.
  # Separate loop so won't get an error if any files are moved due to errors.
  for item in os.listdir():
  # Displays a progress count because this step can take a long time.
    tarzip_count += 1
    print(f'Tar/zipping AIP {tarzip_count} of {total}.')
    subprocess.run(f'perl {prepare_bag} {item} {aip_staging}/aips-ready-to-ingest/', shell=True)

# Checks every zipped AIP for temporary files.
# We have had .DS_Store present in zipped AIPs, even though they are deleted before zipping.
zip_folder = f'{aip_staging}/aips-ready-to-ingest/'
os.chdir(zip_folder)
zip_total = len(os.listdir(zip_folder))
zip_count = 0
for zip_file in os.listdir('.'):
    zip_count += 1
    print(f'Checking for temporary files in zipped AIP {zip_count} of {zip_total}.')
    if zip_file.endswith('.tar'):
        with tarfile.open(zip_file) as tar:
            file_paths_list = tar.getnames()
    elif zip_file.endswith('.tar.bz2'):
        with bz2.BZ2File(zip_file, 'rb') as bz2_file:
            with tarfile.open(fileobj=bz2_file) as tar:
                file_paths_list = tar.getnames()
    else:
        print(f"Cannot check {zip_file} for temp files. Does not end in .tar or .tar.bz2")
        continue

    # If there is a temp file (file name starts with "."), move the zipped AIP to an error folder.
    # It moves the zipped AIP as soon as a temp file is found and does not check for more.
    for file_path in file_paths_list:
        file_name = re.split(r"\\|/", file_path)[-1]
        if file_name.startswith('.'):
            print(f'Hidden file found: {file_path}')
            move_error('temp_in_zip', zip_file)
            break
