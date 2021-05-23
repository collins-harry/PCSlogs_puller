# -*- coding: utf-8 -*-
"""
Created on 23/05/2021 18:25:56

    UI file for finding and downloading zipped csv files and processing them

@author: Harry Collins
"""

import sys
import os
import shutil
import zipfile
from PyQt5 import QtCore, QtGui, uic, QtWidgets

path = r"C:\Users\hcoll\Downloads\FL_insurance_sample.csv.zip"
# shutil.copy2(path, "./zipped_csv.zip")
os.system(r"powershell -ExecutionPolicy Bypass Expand-Archive -Path .\zipped_csv.zip -DestinationPath .\folder")

qtCreatorFile = "layout.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

        
class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QAbstractItemView
        #signal and slots for the ui
        self.folderselect.clicked.connect(self.sFold)
        self.zipfiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.zipview.clicked.connect(self.showDescription)
        self.remove.clicked.connect(self.removeSelected)

        self.UserList.clicked.connect(self.populateSelection)
        self.FolderList.clicked.connect(self.populateSelection)
        
    def populateSelection(self):
        # populates variables with what has been selected by the user
        selected_user_list = self.UserList.selectedItems()
        if len(selected_user_list) == 0:
            print("Need to select user")
        else:
            selected_user = selected_user_list[0].text()
            print(selected_user)

        selected_folder_list = self.FolderList.selectedItems()
        if len(selected_folder_list) == 0:
            print("Need to select Folder")
        else:
            selected_folder = selected_folder_list[0].text()
            print(selected_folder)



    def sFold(self):
        #Populates the list with the zip files present in the dir
        self.folder.setText(QtWidgets.QFileDialog.getExistingDirectory())
        for f in os.listdir(self.folder.toPlainText()):
            if os.path.isfile(os.path.join(self.folder.toPlainText(),f)):
                self.zipfiles.addItem(f)
    
    def showDescription(self,item):
        self.description.clear()
        #Gets the description file from the scatter.zip
        f = self.zipfiles.selectedItems()
        for fn in f:
            print(fn.text())
            path = os.path.join(self.folder.toPlainText(),fn.text())
            zf = zipfile.ZipFile(path,'r')
            self.description.append(str(zf.read("DESCRIPTION.txt")))
        
    def removeSelected(self):
        #removes the desired file, quick message to double check.
        reply = QtWidgets.QMessageBox.question(self, 'Alert!!', "Do you wish to remove this Zip file?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            f = self.zipfiles.currentItem().text()
            self.zipfiles.takeItem(self.zipfiles.row(self.zipfiles.currentItem()))
            path = os.path.join(self.folder.toPlainText(),f)
            os.remove(path)
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Main()
    window.show()
    app.exec_()
