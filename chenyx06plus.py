# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CHENyx06plus
                                 A QGIS plugin
 CHENyx06+
                              -------------------
        begin                : 2015-09-22
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Stefan Ziegler
        email                : stefan.ziegler@bd.so.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from chenyx06plus_dialog import CHENyx06plusDialog
from settings_dialog import SettingsDialog
import os.path


class CHENyx06plus:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # QGIS map canvas
        self.canvas = self.iface.mapCanvas()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CHENyx06plus_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.settings = QSettings("CatAIS","CHENyx06plus")

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.menu = QMenu()
        self.menu.setTitle(self.tr("CHENyx06+"))

        self.projects_menu = QMenu(self.tr("Projects"))
        self.change_settings = QAction(self.tr("Settings"), self.iface.mainWindow())

        self.menu.addMenu(self.projects_menu)
        self.menu.addSeparator()
        self.menu.addAction(self.change_settings)

        menubar = self.iface.mainWindow().menuBar()
        actions = menubar.actions()
        last_action = actions[len(actions) - 1]
        menubar.insertMenu(last_action, self.menu)

        self.change_settings.triggered.connect(self.do_change_settings)

        # Load existing projects into projects menu.
        self.add_projects_to_menu()


    # TODO: Connect to add/change geometrie/attributes signals of projects layer.
    # -> update menu and everythin else.


    # TODO: wahrscheinlich suchen ob project layer geladen ist und signale anhängen.

    # TODO: aktives projekt wählen.

    def add_projects_to_menu(self):
        # After changing the projects database we need to update the
        # the menu and clear the existing entries.
        # But the 'manage project' action is always available.
        self.projects_menu.clear()
        self.manage_projects = QAction(self.tr("Manage projects"), self.iface.mainWindow())
        self.manage_projects.triggered.connect(self.do_manage_projects)
        self.projects_menu.addAction(self.manage_projects)
        self.projects_menu.addSeparator()

        projects_database = self.settings.value("options/general/projects_database")
        layer = QgsVectorLayer(projects_database, self.tr("Projects"), "ogr")

        # TODO: better exception handling.
        if not layer.isValid():
            print "Layer failed to load!"
            return

        if layer.featureCount() == 0:
            return

        project_names = []
        iter = layer.getFeatures()
        for feature in iter:
            project_name = feature.attribute("gemeinde")
            project_names.append(project_name)

        project_names.sort()
        for project_name in project_names:
            action = QAction(unicode(project_name), self.iface.mainWindow())
            self.projects_menu.addAction(action)
            # TODO: connect to signal...

        del layer

    def do_change_settings(self):
        dlg_settings = SettingsDialog()
        dlg_settings.show()
        dlg_settings.projectsDatabaseHasChanged.connect(self.do_load_projects_database)
        result = dlg_settings.exec_()

    def do_manage_projects(self):
        projects_database = self.settings.value("options/general/projects_database")

        # Do not load projects database (layer) if it's already there.
        found = False
        root = QgsProject.instance().layerTreeRoot()
        for node in root.findLayers():
            if node.layer().type() == QgsMapLayer.VectorLayer:
                if node.layer().source() == projects_database:
                    node.setVisible(Qt.Checked)
                    layer = node.layer()

        if not layer:
            layer = self.iface.addVectorLayer(projects_database, self.tr("Projects"), "ogr")

        if not layer.isValid():
            print "Layer failed to load!"
            return

        layer_node = root.findLayer(layer.id())
        if layer_node:
            layer_node.setVisible(Qt.Checked)

        # Zoom to layer extent.
        self.zoom_to_layer(layer)

        # Connect to signal for the case somethings changed in the layer.
        layer.editingStopped.connect(self.projects_layer_modified)

    def projects_layer_modified(self):
        print "fffffuuuuubar"

    def zoom_to_layer(self, layer):
        rect = layer.extent()
        rect.scale(1.2)
        self.canvas.setExtent(rect)
        self.canvas.refresh()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        pass

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CHENyx06plus', message)
