#!/usr/bin/python

import sys

'''
git clone https://github.com/trucomanx/WorkingWithFiles.git
cd WorkingWithFiles/src
python setup.py sdist
pip3 install dist/WorkingWithFiles-*.tar.gz
'''
import WorkingWithFiles as rnfunc

################################################################################
## python clf_csv_gen.py --format .png --csv-file labels.csv --base-dir /my/path
################################################################################
csv_file='test_labels.csv';
base_dir='/mnt/boveda/DATASETs/FACE-EMOTION/mcfer_v1.0/archive/test';
default_format=['.png'];

format_list=[];
for n in range(len(sys.argv)):
    if sys.argv[n]=='--csv-file':
        csv_file=sys.argv[n+1];
    if sys.argv[n]=='--base-dir':
        base_dir=sys.argv[n+1];
    if sys.argv[n]=='--format':
        format_list.append(sys.argv[n+1]);

if len(format_list)==0:
    format_list=default_format.copy()

print('')
print('   csv_file:',csv_file)
print('   base_dir:',base_dir)
print('format_list:',format_list)
print('')

rnfunc.generate_csv_file_from_dir_structure(base_dir,format_list,csv_file);

