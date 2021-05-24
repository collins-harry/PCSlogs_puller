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
import time
from pathlib import Path
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
# \\alpfile3.al.intel.com\sdx_ods\program\1274\eng\hdmtprogs\adl_sds\hcollins 
# \\s46file1.cd.intel.com\sdx\program\1274\eng\hdmtprogs\adl_sds\hcollins\ 

qtCreatorFile = resource_path("layout.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        QtWidgets.QAbstractItemView
        # Options to populate GUI boxes with 
        self.user_options = ["ods","cd"]
        self.folder_options = ["SDX620","SDX618","SDX117","SDX114"]
        self.custom_folder_options = {
            "ods": ["SDX117","SDX114"],
            "cd" : ["SDX620","SDX618"],
        }
        self.site_address= {
            "ods": r"\\alpfile3.al.intel.com\sdx_ods",
            "cd" : r"\\s46file1.cd.intel.com\sdx",
        }
        
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
        self.progressBar.setVisible(True)

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
            
            # \\alpfile3.al.intel.com\sdx_ods\program\1274\eng\hdmtprogs\adl_sds\hcollins 
            # \\s46file1.cd.intel.com\sdx\program\1274\eng\hdmtprogs\adl_sds\hcollins\ 
            i_drive = self.site_address[self.selected_user]

            self.folder_path = rf"{i_drive}\PCSThermalLog\{self.selected_folder}"
            print(self.folder_path)

    def enable_progress_bar(self):
        print("turning on progress bar")
        self.progressBar.setVisible(True)
        print("progress bar on")

    def disable_progress_bar(self):
        self.progressBar.setVisible(False)
    
    def search_path_for_zip_files(self):
        #Populates the list with the zip files present in the dir
        if self.folder_path is None:
            print("Folder path is not created due to not all required options being selected, please select all required options")
            return
        self.enable_progress_bar()

        print(self.folder_path)
        cmd = r'dir /o-d /tc "\\alpfile3.al.intel.com\sdx_ods\PCSThermalLog\SDX117"'
        stdout = subprocess.check_output(cmd, shell=True,text=True)
        stdout_splitted = stdout.split()[14:]

        result = []
        for i in range(0,len(stdout_splitted)-1,4):
            sub_result = []
            for j in range(4):
                sub_result.append(stdout_splitted[i+j])
            result.append(sub_result)

        result = result[:-4]

        for file in result:
            print(file)

        # os.system(r"dir /o-d")
        # files = sorted(Path(self.folder_path).iterdir(), key=os.path.getmtime)
        # files = sorted(os.walk)
        # print("\n", "FILES:\n", files)
        # path_files = os.listdir(self.folder_path)
        # files = glob.glob(os.path.expanduser(self.folder_path+r"\*"))
        # with os.scandir(self.folder_path) as pcslog_dir:
        #     sorted_by_mtime_descending = sorted(pcslog_dir, key=lambda t: -os.stat(t).st_mtime)
                # info = pcslog.stat()
                # print(info.st_mtime

        # sorted_by_mtime_descending = sorted(files, key=lambda t: -os.stat(t).st_mtime)
        # print("\n", "SORTEDFILES:\n", sorted_by_mtime_descending)
        self.zipFilesList.clear()
        for file in result:
            file_string = " ".join([file[3],file[1],file[0]])
            print(file_string)
            self.zipFilesList.addItem(file_string)
        # self.progressBar.setVisible(False)

    def process_zip_files(self):
        self.selected_zip_files = self.zipFilesList.selectedItems()
        for zip_file in self.selected_zip_files:
            zip_file_text = zip_file_path_qt.text()
            zip_file_name = zip_file_text.split()[0]

            print("zip_file_path: ", zip_file_path)
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
