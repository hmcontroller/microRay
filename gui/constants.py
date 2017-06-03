# -*- encoding: utf-8 -*-
from PyQt4 import QtGui


VERSION_NUMBER = 1

MRAY_URI = "http://intern.zeitraffer-aufnahmen.de/mRay"
MRAY_VERSION_FILE = MRAY_URI + "/currentVersion.txt"
MRAY_ONLINE_HELP = MRAY_URI + "/docs/index.html"
MRAY_WEBSITE = MRAY_URI + "/index.html"

AVAILABLE_FRAMEWORKS = [
    {"macroName": "MBED_2_UDP", "displayName": u"Mbed 2 UDP", "interface": "UDP"},
    {"macroName": "MBED_2_SERIAL", "displayName": u"Mbed 2 Serial", "interface": "SERIAL"},
    {"macroName": "MBED_OS_UDP", "displayName": u"Mbed OS UDP", "interface": "UDP"},
    {"macroName": "MBED_OS_SERIAL", "displayName": u"Mbed OS Serial", "interface": "SERIAL"},
    {"macroName": "ARDUINO_UDP", "displayName": u"Arduino UDP", "interface": "UDP"},
    {"macroName": "ARDUINO_SERIAL", "displayName": u"Arduino Serial", "interface": "SERIAL"}
]

RELATIVE_PATH_TO_APPLICATION_SETTINGS = "applicationSettings.json"

CHECK_BOX_FONT = QtGui.QFont()
CHECK_BOX_FONT.setPointSize(8)

USER_INPUT_WARNING_COLOR = QtGui.QColor(255, 165, 0)
CONFIRMATION_TIMEOUT_WARNING_COLOR = QtGui.QColor(210, 0, 0)
# NEGATIVE_CONFIRMATION_WARNING_COLOR = QtGui.QColor(50, 200, 50)
NEGATIVE_CONFIRMATION_WARNING_COLOR = QtGui.QColor(210, 30, 0)

HOVER_COLOR = QtGui.QColor(200, 200, 200)
MOUSE_DOWN_COLOR = QtGui.QColor(150, 150, 150)

PENDING_VALUE_COLOR = QtGui.QColor(210, 0, 0)

CABLE_PEN = QtGui.QPen()
CABLE_PEN.setColor(QtGui.QColor(0, 0, 0))
CABLE_PEN.setCosmetic(True)
CABLE_PEN.setWidth(2)

