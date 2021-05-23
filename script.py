# -*- coding: utf-8 -*-
"""
Created on 23/05/2021 18:25:56

    UI file for finding and downloading zipped csv files and processing them

@author: Harry Collins
"""
import sys
import os
import shutil
# import zipfile
import re
import glob
from PyQt5 import QtCore, QtGui, uic, QtWidgets

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

qtCreatorFile = resource_path("layout.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QAbstractItemView
        
        # Options to populate GUI boxes with 
        self.user_options = ["hcoll"]
        self.folder_options = ["Documents","Downloads"]
        
        self.populateGUIboxes()

        #variables
        self.selected_user = None
        self.selected_folder = None
        self.selected_zip_files = None
        self.folder_path = None


        #signal and slots for the ui
        self.UserList.clicked.connect(self.populateSelection)
        self.FolderList.clicked.connect(self.populateSelection)
        self.folderselectbutton.clicked.connect(self.search_path_for_zip_files)

        self.zipFilesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.zipselectbutton.clicked.connect(self.process_zip_files)

        self.remove.clicked.connect(self.removeSelected)

    def populateGUIboxes(self):
        print("populating GUI boxes")
        for user in self.user_options:
            self.UserList.addItem(user)
        for folder in self.folder_options:
            self.FolderList.addItem(folder)
        
    def populateSelection(self):
        # populates variables with what has been selected by the user
        selected_user_list = self.UserList.selectedItems()
        if len(selected_user_list) == 0:
            print("Need to select user")
        else:
            self.selected_user = selected_user_list[0].text()
            print(self.selected_user)

        selected_folder_list = self.FolderList.selectedItems()
        if len(selected_folder_list) == 0:
            print("Need to select Folder")
        else:
            self.selected_folder = selected_folder_list[0].text()
            print(self.selected_folder)
        
        if self.selected_user is not None and self.selected_folder is not None:
            self.folder_path = rf"C:\Users\{self.selected_user}\{self.selected_folder}"
            print(self.folder_path)

    def search_path_for_zip_files(self):
        #Populates the list with the zip files present in the dir
        if self.folder_path is None:
            print("Folder path is not created due to not all required options being selected, please select all required options")
            return
        print(self.folder_path)
        # path_files = os.listdir(self.folder_path)
        files = glob.glob(os.path.expanduser(self.folder_path+r"\*"))
        sorted_by_mtime_descending = sorted(files, key=lambda t: -os.stat(t).st_mtime)

        self.zipFilesList.clear()
        for f in sorted_by_mtime_descending:
            if os.path.isfile(f):
                if re.match(r".*\.zip", f):
                    print(f)
                    self.zipFilesList.addItem(f)

    def process_zip_files(self):
        self.selected_zip_files = self.zipFilesList.selectedItems()
        for zip_file_path_qt in self.selected_zip_files:
            zip_file_path = zip_file_path_qt.text()
            print("zip_file_path: ", zip_file_path)
            zip_file_name = os.path.basename(zip_file_path)
            print("zip_file_name: ", zip_file_name)

            shutil.copy2(zip_file_path, f"./csv_{zip_file_name}")
            print("zip file copied over ")
            unzipped_folder_name = zip_file_name[:-8]
            print("unzipping folder...")
            os.system(rf"powershell -ExecutionPolicy Bypass Expand-Archive -Path .\csv_{zip_file_name} -DestinationPath .\{unzipped_folder_name} -Force")
            print("Finished, unzipped folder name: ", unzipped_folder_name)
    
    def showDescription(self,item):
        self.description.clear()
        #Gets the description file from the scatter.zip
        f = self.zipFilesList.selectedItems()
        for fn in f:
            print(fn.text())
            path = os.path.join(self.folder.toPlainText(),fn.text())
            zf = zipfile.ZipFile(path,'r')
            self.description.append(str(zf.read("DESCRIPTION.txt")))
        
    def removeSelected(self):
        #removes the desired file, quick message to double check.
        reply = QtWidgets.QMessageBox.question(self, 'Alert!!', "Do you wish to remove this Zip file?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            f = self.zipFilesList.currentItem().text()
            self.zipFilesList.takeItem(self.zipFilesList.row(self.zipFilesList.currentItem()))
            path = os.path.join(self.folder.toPlainText(),f)
            os.remove(path)
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    window = Main()
    window.show()
    app.exec_()
