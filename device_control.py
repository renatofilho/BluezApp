#!/usr/bin/python

from PySide.QtCore import QObject, Slot


class DeviceControl(QObject):
    def __init__(self, model, parent = None):
        super(DeviceControl, self).__init__(parent)
        self._model = model

    @Slot(int)
    def deviceSelected(self, index):
        d = self._model.getDevice(index)
        print "Device selected", self._model.getDevice(index)
        d.getServices()
