import os
import subprocess

for item in os.listdir():
  
  #should have done rename to take off .xml before named .csv.  Cleaner that way.
  #also shouldn't have put the column header in the stylesheet because then have to delete out of everything.  
  subprocess.run(f'java -cp H:/python/python_aip-script/saxon/saxon9he.jar net.sf.saxon.Transform -s:{item} -xsl:C:/Users/hansona/Desktop/name_date.xsl -o:{item}.csv', shell=True)
  
for csv in os.listdir():
  if csv.endswith('.csv'):
    print(csv)