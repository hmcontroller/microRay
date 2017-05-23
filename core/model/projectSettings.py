# -*- encoding: utf-8 -*-

from PyQt4 import QtCore


class ProjectSettings(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(ProjectSettings, self).__init__()
        self._projectName = u""
        self._controllerLoopCycleTimeInUs = 5000
        self._computerIP = "192.168.0.133"
        self._controllerIP = "192.168.0.15"
        self._udpPort = 10000
        self._comPortDescription = ""
        self._controllerFrameworkAndInterface = "mbed_udp"
        self._tabSettingsDescriptions = list()
        self._pathToControllerCodeFolder = u""
        self._openedFrom = ""
        self._unsavedChanges = False

    def somethingChanged(self):
        self._unsavedChanges = True
        self.changed.emit(self)

    @property
    def projectName(self):
        return self._projectName

    @projectName.setter
    def projectName(self, value):
        self._projectName = value
        self.somethingChanged()

    @property
    def controllerLoopCycleTimeInUs(self):
        return self._controllerLoopCycleTimeInUs

    @controllerLoopCycleTimeInUs.setter
    def controllerLoopCycleTimeInUs(self, value):
        self._controllerLoopCycleTimeInUs = value
        self.somethingChanged()

    @property
    def computerIP(self):
        return self._computerIP

    @computerIP.setter
    def computerIP(self, value):
        self._computerIP = value
        self.somethingChanged()

    @property
    def controllerIP(self):
        return self._controllerIP

    @controllerIP.setter
    def controllerIP(self, value):
        self._controllerIP = value
        self.somethingChanged()

    @property
    def udpPort(self):
        return self._udpPort

    @udpPort.setter
    def udpPort(self, value):
        self._udpPort = value
        self.somethingChanged()

    @property
    def comPortDescription(self):
        return self._comPortDescription

    @comPortDescription.setter
    def comPortDescription(self, value):
        self._comPortDescription = value
        self.somethingChanged()

    @property
    def controllerFrameworkAndInterface(self):
        return self._controllerFrameworkAndInterface

    @controllerFrameworkAndInterface.setter
    def controllerFrameworkAndInterface(self, value):
        self._controllerFrameworkAndInterface = value
        self.somethingChanged()

    @property
    def tabSettingsDescriptions(self):
        return self._tabSettingsDescriptions

    @tabSettingsDescriptions.setter
    def tabSettingsDescriptions(self, value):
        self._tabSettingsDescriptions = value
        self.somethingChanged()


    @property
    def pathToControllerCodeFolder(self):
        return self._pathToControllerCodeFolder

    @pathToControllerCodeFolder.setter
    def pathToControllerCodeFolder(self, value):
        self._pathToControllerCodeFolder = value
        self.somethingChanged()

    @property
    def openedFrom(self):
        return self._openedFrom

    @openedFrom.setter
    def openedFrom(self, value):
        self._openedFrom = value
        self.somethingChanged()

    @property
    def unsavedChanges(self):
        return self._unsavedChanges

    @unsavedChanges.setter
    def unsavedChanges(self, value):
        self._unsavedChanges = value

        # prevent setting unsavedChanges to True ;)
        self.changed.emit(self)