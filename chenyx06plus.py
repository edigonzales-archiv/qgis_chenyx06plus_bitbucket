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
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from chenyx06plus_dialog import CHENyx06plusDialog
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

        # Create the dialog (after translation) and keep reference
        self.dlg = CHENyx06plusDialog()

        # Declare instance attributes
        self.actions = []
        #self.menu = self.tr(u'&CHENyx06+')
        # TODO: We are going to let the user set this up in a future iteration
        #self.toolbar = self.iface.addToolBar(u'CHENyx06plus')
        #self.toolbar.setObjectName(u'CHENyx06plus')

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


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""


        self.menu = QMenu()
        self.menu.setTitle(self.tr("CHENyx06+"))

        self.load_chenyx06 = QAction(self.tr("Load CHENyx06 data"), self.iface.mainWindow())
        self.menu.addAction(self.load_chenyx06)

        menubar = self.iface.mainWindow().menuBar()
        actions = menubar.actions()
        last_action = actions[len(actions) - 1]
        menubar.insertMenu(last_action, self.menu)




    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        pass


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
