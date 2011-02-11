#!/usr/bin/python

from PySide.QtCore import QObject, Signal, QUrl, Slot
from PySide.QtGui import QApplication
from agent import BluezAgent
from service import BluezService

import os
import sys
import dbus
import dbus.mainloop.glib


class BluezDevice(object):
    def __init__(self, addr, properties, parent):
        self._addr = addr
        self._prop = properties
        self._manager = parent
        self._busy = False
        self._bus = None

    def update(self, properties):
        update = False
        for key in properties.keys():
            if (key not in self._prop.keys()) or (self._prop[key] != properties[key]):
                self._prop[key] = properties[key]
                update = True
        return update

    def address(self):
        return self._addr

    def path(self):
        if self._bus:
            return self._bus.path

    def name(self):
        if not 'Name' in self._prop:
            return self.address()
        else:
            return self._prop['Name']

    def setPaired(self, value):
        self._prop['Paired'] = value

    def paired(self):
        if not 'Paired' in self._prop:
            return False
        else:
            return self._prop['Paired']

    def useLagacyPairing(self):
        if not 'LegacyPairing' in self._prop:
            return False
        else:
            return self._prop['LegacyPairing']

    def isLowEnergy(self):
        return "Broadcaster" in self._prop.keys()

    def setTrusted(self, value):
        self._prop['Trusted'] = value

    def trusted(self):
        if 'Trusted' in self._prop.keys():
            return self._prop['Trusted']
        return False

    def iconName(self):
        if 'Icon' in  self._prop.keys():
            icon_name = './qml/icons/%s.png' % self._prop['Icon']
            if not os.path.exists(icon_name):
                icon_name = './qml/icons/unknow.png'
        else:
            icon_name = './qml/icons/unknow.png'

        return QUrl.fromLocalFile(icon_name)

    def getServices(self):
        services = []
        if 'UUIDs' in self._prop:
            return self._prop['UUIDs']
        return []

    def busy(self):
        return self._busy

    def setBusy(self, busy):
        self._busy = busy

    def _createDevice(self):
        if not self._bus:
            self._bus = self._dbus.Interface(self._bus.get_object("org.bluez", devPath),
                                                            "org.bluez.Device")

    def _setBusDevice(self, bus):
        self._bus = bus

    def __eq__(self, other):
        return self._addr == other._addr

    serivceDiscovered = Signal(str)


class DeviceManager(QObject):
    def __init__(self, adapterName=None, parent=None):
        QObject.__init__(self, parent)
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        self._devices = {}
        self._devPathToAddress = {}

        self._bus = dbus.SystemBus()
        self._manager = dbus.Interface(self._bus.get_object("org.bluez", "/"),
                                       "org.bluez.Manager")

        adapter = None
        if adapterName:
            try:
                adapter = self._manager.FindAdapter(adapterName)
            except:
                print "Adaper %s not found" % adapterName

        if not adapter:
            print "Using default adapter"
            adapter = self._manager.DefaultAdapter()

        self._adapter = dbus.Interface(self._bus.get_object("org.bluez",
                                       adapter),
                                       "org.bluez.Adapter")
        self._bus.add_signal_receiver(self._onDeviceFound,
                                      dbus_interface = "org.bluez.Adapter",
                                      signal_name = "DeviceFound")
        self._bus.add_signal_receiver(self._onDeviceDisappeared,
                                      dbus_interface = "org.bluez.Adapter",
                                      signal_name = "DeviceDisappeared")

    def getDevice(self, addr):
        return self._devices[addr]

    def deviceCount(self):
        return len(self._devices)

    def start(self, timeout=1000):
        self._adapter.StartDiscovery()

    @Slot(str, str)
    def connectTo(self, addr, pinCode=None):
        if addr in self._devices:
            self._connectingDevice = self._devices[addr]
            self._connectionStart(addr)
            self._adapter.StopDiscovery()
            path = '/app/PySideBluez'
            self._agent = BluezAgent(self._bus, path, self, pinCode)
            self._adapter.CreatePairedDevice(addr, path, 'DisplayYesNo',
                                             reply_handler=self._onCreateDeviceReply,
                                             error_handler=self._onCreateDeviceError)

    def _connectionStart(self, addr):
        if addr in self._devices:
            dev = self._devices[addr]
            if not dev.busy():
                dev.setBusy(True)
                self.deviceUpdate.emit(dev)

    def _connectionFinish(self, addr):
        if addr in self._devices:
            dev = self._devices[addr]
            if dev.busy():
                dev.setBusy(False)
                self.deviceUpdate.emit(dev)

    def _registerDevicePath(self, devPath):
        dev = None
        busDevice = dbus.Interface(self._bus.get_object("org.bluez", devPath),
                                                        "org.bluez.Device")
        properties = busDevice.GetProperties()
        addr = properties["Address"]
        if addr in self._devices:
            dev = self._devices[addr]
            dev._setBusDevice(busDevice)
            dev.update(properties)
            self._devPathToAddress[devPath] = dev

        return dev

    def _getDeviceByPath(self, devPath):
        if devPath in self._devPathToAddress:
            return self._devPathToAddress[devPath]
        else:
            return self._registerDevicePath(devPath)

    def _onCreateDeviceReply(self, devPath):
        print "Device Created", devPath
        dev = self._getDeviceByPath(devPath)
        if dev:
            dev.setBusy(False)
            self.deviceUpdate.emit(dev)
        self._connectingDevice = None

    def _onCreateDeviceError(self, error):
        print "Create error:", error
        self.deviceCreateError.emit(error)
        self._connectingDevice.setBusy(False)
        self.deviceUpdate.emit(self._connectingDevice)
        self._connectingDevice = None

    def _onDeviceDisappeared(self, address):
        if address in self._devices:
            dev = self._devices[address]
            self.deviceDisappeared.emit(dev)
            for (k, v) in zip(self._devPathToAddress):
                if v == dev:
                    del self._devPathToAddress[k]
                    break
            del self._devices[address]

    def _onDeviceFound(self, address, properties):
        if address not in self._devices.keys():
            dev = BluezDevice(address, properties, self)
            self._devices[address] = dev
            self.deviceFound.emit(dev)
            if dev.paired():
                path = self._adapter.FindDevice(address)
                self._registerDevicePath(path)
        else:
            dev = self._devices[address]
            if dev.update(properties):
                self.deviceUpdate.emit(dev)

    deviceUpdate = Signal(object)
    deviceFound = Signal(object)
    deviceDisappeared = Signal(object)
    deviceCreated = Signal(object)
    deviceCreateError = Signal(str)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = DeviceManager()
    manager.start()
    app.exec_()
