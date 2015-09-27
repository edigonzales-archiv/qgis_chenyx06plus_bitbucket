# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'settings_dialog_base.ui'))


class SettingsDialog(QDialog, FORM_CLASS):

    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)

        self.settings = QSettings("CatAIS","CHENyx06plus")
        self.projects_database = self.settings.value("options/general/projects_database")
        self.projects_database_path = QFileInfo(self.projects_database).absolutePath()
        self.projects_root_directory = self.settings.value("options/general/projects_root_directory")

        self.lineEditProjectsDatabase.setText(self.projects_database)
        self.lineEditProjectsRootDir.setText(self.projects_root_directory)

        QWidget.setTabOrder(self.lineEditProjectsDatabase, self.lineEditProjectsRootDir)

    @pyqtSignature("on_btnBrowseProjectsDatabase_clicked()")
    def on_btnBrowseProjectsDatabase_clicked(self):
        file = QFileDialog.getOpenFileName(self, self.tr("Choose projects database"), self.projects_database_path,  "GPKG (*gpkg *.sqlite *.db *.DB)")
        file_info = QFileInfo(file)
        self.lineEditProjectsDatabase.setText(file_info.absoluteFilePath())

    @pyqtSignature("on_btnBrowseProjectsRootDir_clicked()")
    def on_btnBrowseProjectsRootDir_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, self.tr("Choose projects root directory"), self.projects_root_directory)
        dir_info = QFileInfo(dir)
        self.lineEditProjectsRootDir.setText(dir_info.absoluteFilePath())

    def accept(self):
        self.settings.setValue("options/general/projects_database", self.lineEditProjectsDatabase.text().strip())
        self.settings.setValue("options/general/projects_root_directory", self.lineEditProjectsRootDir.text().strip())

        self.projectsDatabaseHasChanged.emit()

        self.close()

    def tr(self, message):
        return QCoreApplication.translate('CHENyx06plus', message)
