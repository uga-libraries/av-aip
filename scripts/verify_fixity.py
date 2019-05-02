# Purpose: verify fixity for files with sidecar (workflow is MKV or MOV).
# Dependencies: checksumthing, md5deep

import os
import subprocess
from variables import *


print('\n>>>Verifying fixity...\n')

# Makes a manifest from the existing sidecar files.
# NOT TESTED: couldn't get checksumthing configured right on my machine (AH)
subprocess.run(f'checksumthing -i "{aips_directory}" -ie .md5 -t md5 -c lower -r -post "fullpath" -o "{aips_directory}"/oldmd5manifest.txt', shell=True)

for item in os.listdir():

  #Skips the manifest, which are produced by the previous step, and temporary files (their fixity often changes).
  if item == 'oldmd5manifest.txt' or item.startswith('._'):
    continue

  if item.endswith('.mov') or item.endswith('.mkv'):
    # Compares the current MD5 to the manifest.
    md5deep_result = subprocess.run(f'md5deep -X "{aips_directory}"/oldmd5manifest.txt "{item}"', stdout=subprocess.PIPE, shell=True)

    # Moves the AIP, including the associated sidecar file, to another location on aip_staging if the fixity has changed.  
    # md5deep has an empty stdout if the MD5 matched. If it didn't match, stdout would have the current fixity and full filepath.
    # md5deep does not store anything in stderr, which is what we generally use to test if something has errors or not.
    if not "stdout=b''" in str(md5deep_result):
      move_error('fixity_changed', item)
      move_error('fixity_changed', f'{item}.md5')

	
# Delete sidecar files and the manifest, which are no longer needed.
# Separate loop so won't get an error if any sidecar files are moved due to errors.
for item in os.listdir():
  if item.endswith('.md5') or item == 'oldmd5manifest.txt':
    os.remove(item)
