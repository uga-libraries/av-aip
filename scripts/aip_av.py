# Usage: python3 path/to/aip_av.py workflow_type path/to/aips_directory department

# workflow_type choices are: 'dpx', 'mkv', 'mkv-filmscan', 'mov', 'mxf', 'wav'

# Prepares audiovisual data for ingest into the UGA Libraries Digital Preservation Storage System as an AIP by running a series of scripts in sequence:

#  1. duplicate_check.py checks that an aip with the same aip-id isn't already in local storage.
#  2. verify_fixity.py verifies checksums for AV with sidecar files.
#  3. aip_directory.py creates the AIP directory structure and moves files to subfolders.
#  4. metadata.py creates mediainfo XML and other metadata files if applicable.
#  5. master.py creates master.xml using XSLT on mediainfo XML; validates master.xml.
#  6. bag.py bags and renames the AIP; validates the bag.
#  7. tar_zip.py uses prepare_bag script to tar and zip the AIP.
#  8. manifest_ingest.py creates MD5 manifest; moves tarred and zipped bags to the ingest server.

# If errors are encountered during defined points in the process, the AIP is moved to a folder with the name of the error and no further processing is done on that AIP.

# Dependencies: bagit.py, checksumthing, ffmpeg, md5deep, mediainfo, mediainfo-to-master.xslt stylesheet, prepare_bag perl script, rsync, saxon xslt processor, xmllint

import os
import subprocess
from variables import *

script_version = 3.0

# Clear the terminal and announce the tool.
os.system('clear')
print(f'Script to prepare AV data for AIP ingest: {workflow} workflow, script version {script_version}.\n')

os.chdir(aips_directory)

# Delete any .DS_Store or Thumbs.db because they cause errors with the scripts and with bag validation.
for root, dirs, files in os.walk('.'):
  for item in files:
    if item == '.DS_Store' or item == '._.DS_Store' or item == 'Thumbs.db':
      os.remove(f'{root}/{item}')

# Run each of the scripts. Need to give the arguments each time or importing variables.py will give validation errors.
# To run a subset of the scripts, make lines you don't want to run a comment by putting # in front.
# Importing variables.py causes the validation checks to run, which is why it is not included below.

# subprocess.run(f'python3 {scripts}/duplicate_check.py {workflow} {aips_directory} {department}', shell=True)

if workflow == 'mkv' or workflow == 'mov' or workflow == 'wav':
  subprocess.run(f'python3 {scripts}/verify_fixity.py {workflow} {aips_directory} {department}', shell=True)

subprocess.run(f'python3 {scripts}/aip_directory.py {workflow} {aips_directory} {department}', shell=True)

subprocess.run(f'python3 {scripts}/metadata.py {workflow} {aips_directory} {department}', shell=True)

subprocess.run(f'python3 {scripts}/master.py {workflow} {aips_directory} {department}', shell=True)

subprocess.run(f'python3 {scripts}/bag.py {workflow} {aips_directory} {department}', shell=True)

subprocess.run(f'python3 {scripts}/tar_zip.py {workflow} {aips_directory} {department}', shell=True)

subprocess.run(f'python3 {scripts}/manifest_ingest.py {workflow} {aips_directory} {department}', shell=True)

print('\nScript is finished running.')
