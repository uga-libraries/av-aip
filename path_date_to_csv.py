# Digital Humanities and Archival Description Experiment
# Written for Python 3.7.0.
# Script to select specified content from each FITS xml metadata file in a target directory and output that content to one combined csv file
# Usage: python script_name target_directory (contains the FITS xml files)

#NOT WORKING FOR ME - got syntax error line 1, column 0 from ET. I thought all I did was delete the fields I'm not using but I guess I did more...

import os
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from sys import argv

errors = []     # create a variable to hold error messages
if len(argv) == 2:        # if we are passed two arguments
    if os.path.exists(argv[1]):     # check if target directory exists
        if os.path.isdir(argv[1]):  # check if target directory is a directory
            target_directory = argv[1]
        else:
            errors.append(f'Target directory "{argv[1]}" is not a directory.')  # if not a directory, add to error messages
    else:
        errors.append(f'Target directory "{argv[1]}" does not exist.')  # if it does not exist, add to error messages
else:
    print("Please specify a target directory")
    exit()

if len(errors) > 0:     # if there are errors, print each error message
  for error in errors:
    print(error)
    exit()

print("Data conversion kung fu in progress...")

# change to directory containing xml input files
os.chdir(target_directory)

# make new directory for csv output file
os.mkdir('../csv_output')

# open csv file for writing
csv_file = open('../csv_output/path-and-date.csv', 'w', newline = '', encoding = 'UTF8')

# create csv writer object
csvwriter = csv.writer(csv_file)

# write header row to csv file
csvwriter.writerow(['file_path', 'date_last_modified'])

# iterate over files in target directory
for file in os.listdir(target_directory):
    # parse XML file and get root of tree
    ET.register_namespace('',"http://hul.harvard.edu/ois/xml/ns/fits/fits_output")
    tree = ET.parse(file)
    root = tree.getroot()

    # for each fits element, find specified children and store as variables to be written to csv row later
    for fits in root.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fits'):

        for filepath in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}filepath'):
            file_path = filepath.text

        # use date last modified as identified by the file system unix time stamp
        for fslastmodified in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fslastmodified'):
            # convert unix time stamp to an integer and then reformat to YYYY
            date_last_modified = datetime.fromtimestamp(int(fslastmodified.text) / 1e3).strftime('%Y')

        # write selected xml text nodes to csv file, one row for each fits entry
        csvwriter.writerow([file_path, date_last_modified])

# close csv file
csv_file.close
print("Script complete")
