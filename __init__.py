# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CHENyx06plus
                                 A QGIS plugin
 CHENyx06+
                             -------------------
        begin                : 2015-09-22
        copyright            : (C) 2015 by Stefan Ziegler
        email                : stefan.ziegler@bd.so.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CHENyx06plus class from file CHENyx06plus.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .chenyx06plus import CHENyx06plus
    return CHENyx06plus(iface)
