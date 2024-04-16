#!/usr/bin/python

import sys
import os
import json

'''
git clone https://github.com/trucomanx/WorkingWithFiles.git
cd WorkingWithFiles/src
python3 setup.py sdist
pip3 install dist/WorkingWithFiles-*.tar.gz
rm -f -r WorkingWithFiles
'''
import WorkingWithFiles as rnfunc

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QWidget,
    QRadioButton,
)



app = QApplication([])
window = QWidget()
window.setWindowTitle("clf_csv_gen")
window.setGeometry(100, 100, 800, 240)


layout = QGridLayout()

## Row pretty label 
layout.addWidget(QLabel("<b>Input:</b>"),0,0)

## Row images directory
base_dir_btn=QPushButton("Base directory:");
base_dir_linedit=QLineEdit('./');
layout.addWidget(base_dir_btn,1,0)
layout.addWidget(base_dir_linedit,1,1)
def on_base_dir_btn_clicked():
    filepath = str(QFileDialog.getExistingDirectory(window, "Select Directory"))
    base_dir_linedit.setText(filepath)

## Row images filetype
file_type_linedit=QLineEdit('.png')
layout.addWidget(QLabel("file type:"),2,0)
layout.addWidget(file_type_linedit,2,1)

## Row pretty label 
layout.addWidget(QLabel("<b>Output:</b>"),3,0)

## Row CSV directory
csv_dir_btn=QPushButton("CSV file directory:")
csv_dir_linedit=QLineEdit('./')
layout.addWidget(csv_dir_btn,4,0)
layout.addWidget(csv_dir_linedit,4,1)
def on_csv_dir_btn_clicked():
    filepath = str(QFileDialog.getExistingDirectory(window, "Select Directory"))
    csv_dir_linedit.setText(filepath)

## Row CSV filename
csv_filename_linedit=QLineEdit('labels.csv')
layout.addWidget(QLabel("CSV filename:"),5,0)
layout.addWidget(csv_filename_linedit,5,1)

## Row category
hlayout = QHBoxLayout();
rb_last = QRadioButton('Last folder name', window);
rb_last.setChecked(False);
rb_first = QRadioButton('First folder name', window);
rb_first.setChecked(True);
hlayout.addWidget(rb_last);
hlayout.addWidget(rb_first);
layout.addWidget(QLabel("Category:"),6,0)
layout.addLayout(hlayout,6,1);

## Row generate_btn
def on_generate_btn_clicked():
    base_dir     = base_dir_linedit.text();
    file_type    = file_type_linedit.text();
    csv_dir      = csv_dir_linedit.text();
    csv_filename = csv_filename_linedit.text();
    
    rb_first_down=rb_first.isChecked();
    
    format_list=[file_type];
    csv_file=os.path.join(csv_dir,csv_filename);
    res,Count=rnfunc.generate_csv_file_from_dir_structure(base_dir,format_list,csv_file,label_first=rb_first_down);
    
    # create json object from dictionary
    json_dat = json.dumps(Count, indent = 4)
    f = open(csv_file+".json","w")
    f.write(json_dat)
    f.close();

    
    alert = QMessageBox()
    alert.setText('found '+str(len(res))+' files with the categories: '+str(Count))
    alert.exec()

generate_btn=QPushButton("Generate")
layout.addWidget(QLabel(" "),7,0)
layout.addWidget(generate_btn,8,0)
window.setLayout(layout)

##
csv_dir_btn.clicked.connect(on_csv_dir_btn_clicked)
base_dir_btn.clicked.connect(on_base_dir_btn_clicked)
generate_btn.clicked.connect(on_generate_btn_clicked)

window.show()
sys.exit(app.exec())



