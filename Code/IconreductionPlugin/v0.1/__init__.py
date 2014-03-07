# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IconReduction
                                 A QGIS plugin
 arrange icons in the menubar
                             -------------------
        begin                : 2014-02-27
        copyright            : (C) 2014 by Marc Schneiter
        email                : schneiter@eclipso.ch
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

def classFactory(iface):
    # load IconReduction class from file IconReduction
    from iconreduction import IconReduction
    return IconReduction(iface)
