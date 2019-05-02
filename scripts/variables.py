# Purpose: defines variables and a function that are used by other aip workflow scripts; validated values of variables taken from arguments.
# Dependencies: none

import os
import sys


# Variables that have a constant value, determined by local machine.
aip_staging = 'INSERT PATH HERE'
ingest_server = 'INSERT PATH HERE'
scripts = 'INSERT PATH HERE'
saxon = 'INSERT PATH HERE'
stylesheet = 'INSERT PATH HERE'
xsd = 'INSERT PATH HERE'
prepare_bag = 'INSERT PATH HERE'


# Variables that are determined from script arguments.
# Tests that each are valid and quits script if any are not valid.
# Can put default values here and make the argument optional by changing the test for the number of arguments (below).
workflow = ''
aips_directory = ''
department = ''

# Starts a list for errors so that can test for all possible errors before quit the script.
# After each test, adds any error message to this list.
errors = []

# Should have 4 arguments: script name, workflow type, path to the aips directory, and department.
# To make some arguments optional, change to: if len(sys.argv) < number of required arguments
if len(sys.argv) != 4:
  errors.append('Incorrect number of arguments.')

# Tests the workflow type, which should be dpx, mkv, mov, or mxf.
if len(sys.argv) > 1:
  workflow_types = ['dpx', 'mkv', 'mov', 'mxf']
  if sys.argv[1] in workflow_types:
    workflow = sys.argv[1]
  else:
    errors.append(f'"{sys.argv[1]}" is not a recognized workflow type {workflow_types}.')

# Tests the aips directory, which should be a valid path.
if len(sys.argv) > 2:
  if os.path.isdir(sys.argv[2]):
    aips_directory = sys.argv[2]
  else:
    errors.append(f'"{sys.argv[2]}" is not a valid directory.')

# Tests the department, which should be bmac or rbrl.
if len(sys.argv) > 3:
  if sys.argv[3] == 'bmac' or sys.argv[3] == 'rbrl':
    department = sys.argv[3]
  else:
    errors.append(f'"{sys.argv[3]}" is not a recognized department code (bmac or rbrl).')


# If there are any errors (the errors list isn't empty), prints the error messages and a usage message and quits the script.
if len(errors) > 0:
  print('The script cannot be run as entered. Please correct the following errors:\n')
  for error in errors:
    print(f'\t*{error}\n')
  print('Script Usage: python3 path/to/aip_av.py workflow_type path/to/aips_directory department\n')
  exit()

  
# Function to move AIPs with errors to a different place on aip_staging so the rest of the script doesn't run on it.
# Makes a folder with the error name, if it doesn't exist already, and moves the AIP there.
# Used in multiple scripts.
def move_error(error_name, item):
  if not os.path.exists(f'{aip_staging}/aips_with_errors/{error_name}'):
    os.makedirs(f'{aip_staging}/aips_with_errors/{error_name}')
  os.replace(item, f'{aip_staging}/aips_with_errors/{error_name}/{item}')
