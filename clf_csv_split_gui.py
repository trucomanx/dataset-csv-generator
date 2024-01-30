#!/usr/bin/python

import sys
import os
import json
from pathlib import Path
import numpy as np

'''
git clone https://github.com/trucomanx/WorkingWithFiles.git
cd WorkingWithFiles/src
python setup.py sdist
pip3 install dist/WorkingWithFiles-*.tar.gz
'''
import WorkingWithFiles as rnfunc


'''
git clone https://github.com/trucomanx/PythonMlTools.git
cd PythonMlTools/src
python setup.py sdist
pip3 install dist/PythonMlTools-*.tar.gz
'''
import PythonMlTools.DataSet.Split as pds

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QDoubleSpinBox,
    QMessageBox,
    QGridLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QWidget,
)



app = QApplication([])
window = QWidget()
window.setWindowTitle("clf_csv_gen")
window.setGeometry(100, 100, 800, 240)


layout = QGridLayout()

layout.addWidget(QLabel("<b>Input:</b>"),0,0)

input_csv_btn=QPushButton("Input csv file:");
input_csv_linedit=QLineEdit('');
layout.addWidget(input_csv_btn,1,0)
layout.addWidget(input_csv_linedit,1,1)
def on_input_csv_btn_clicked():
    default_dir=str(Path.home());
    tmp_str=input_csv_linedit.text();
    if len(tmp_str)>0:
        if os.path.isdir(tmp_str):
            default_dir=str(tmp_str);
        if os.path.isfile(tmp_str):
            default_dir=os.path.dirname(tmp_str);
    
    filters = "csv (*.csv)"
    #selected_filter = "Images (*.png *.xpm *.jpg)"
    filepath, tmp = QFileDialog.getOpenFileName(window,"Open File",default_dir,filters)
    
    input_csv_linedit.setText(filepath)

test_factor_spin=QDoubleSpinBox()
test_factor_spin.setDecimals(2);
test_factor_spin.setRange(0.0,100.0);
test_factor_spin.setSingleStep(0.1);
test_factor_spin.setValue(38.19);
layout.addWidget(QLabel("Test percentage %:"),2,0)
layout.addWidget(test_factor_spin,2,1)

layout.addWidget(QLabel("<b>Output:</b>"),3,0)

csv_out_dir_btn=QPushButton("CSV file directory:")
csv_out_dir_linedit=QLineEdit('./')
layout.addWidget(csv_out_dir_btn,4,0)
layout.addWidget(csv_out_dir_linedit,4,1)
def on_csv_out_dir_btn_clicked():
    default_dir=str(Path.home());
    tmp_str=input_csv_linedit.text();
    if len(tmp_str)>0:
        if os.path.isdir(tmp_str):
            default_dir=str(tmp_str);
        if os.path.isfile(tmp_str):
            default_dir=os.path.dirname(tmp_str);
    
    filepath = str(QFileDialog.getExistingDirectory(window, "Select Directory",default_dir))
    csv_out_dir_linedit.setText(filepath)

csv_train_filename_linedit=QLineEdit('train.csv')
layout.addWidget(QLabel("CSV train filename:"),5,0)
layout.addWidget(csv_train_filename_linedit,5,1)

csv_test_filename_linedit=QLineEdit('test.csv')
layout.addWidget(QLabel("CSV test filename:"),6,0)
layout.addWidget(csv_test_filename_linedit,6,1)

def on_generate_btn_clicked():
    csv_out_dir  = csv_out_dir_linedit.text();
    csv_train_filename = csv_train_filename_linedit.text();
    csv_test_filename  = csv_test_filename_linedit.text();
    
    ########################################
    
    input_csv    = input_csv_linedit.text();
    test_factor  = test_factor_spin.value();
    random_state = 42;
    
    csv_train_file=os.path.join(csv_out_dir,csv_train_filename);
    csv_test_file =os.path.join(csv_out_dir,csv_test_filename);
    
    ########################################
    
    from sklearn.model_selection import train_test_split
    import pandas as pd

    df = pd.read_csv(input_csv)
    y_np=df.iloc[:,-1].to_numpy();
    d_set=list(set(y_np));
    d_lbl=list(range(0,len(d_set)));
    mydict=dict(zip(list(d_set),d_lbl))
    
    y=np.array([mydict[val] for val in y_np]);
    
    
    y_train_id, y_test_id, y_train, y_test = pds.train_test_split_stratify_index(y,
                                                            test_size=test_factor/100.0, 
                                                            random_state=random_state);
    
    df_train = df.iloc[np.uint32(y_train_id).tolist(),:];
    df_test  = df.iloc[np.uint32(y_test_id).tolist(),:];
    
    #print(df_train)
    #print(df_test)
    
    df_train.to_csv(csv_train_file, index=False)  
    df_test.to_csv(csv_test_file, index=False)  
    
    alert = QMessageBox()
    alert.setText('Work end')
    alert.exec()

generate_btn=QPushButton("Generate")
layout.addWidget(QLabel(" "),7,0)
layout.addWidget(generate_btn,8,0)
window.setLayout(layout)

csv_out_dir_btn.clicked.connect(on_csv_out_dir_btn_clicked)
input_csv_btn.clicked.connect(on_input_csv_btn_clicked)
generate_btn.clicked.connect(on_generate_btn_clicked)

window.show()
sys.exit(app.exec())



