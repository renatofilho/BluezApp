from PySide.QtCore import QAbstractListModel, Qt, QModelIndex, Slot, Signal

class DeviceListModel(QAbstractListModel):
    DEVICE_NAME_ROLE = Qt.UserRole + 1
    DEVICE_PAIRED_ROLE = DEVICE_NAME_ROLE + 1
    DEVICE_TRUSTED_ROLE = DEVICE_NAME_ROLE + 2
    DEVICE_ICON_ROLE = DEVICE_NAME_ROLE + 3
    DEVICE_ADDRESS_ROLE = DEVICE_NAME_ROLE + 4
    DEVICE_BUSY_ROLE = DEVICE_NAME_ROLE + 5
    DEVICE_LOW_ENERGY_ROLE = DEVICE_NAME_ROLE + 6

    def __init__(self, manager, parent=None):
        super(DeviceListModel, self).__init__(parent)
        self._manager = manager
        self._manager.deviceFound.connect(self._onDeviceFound)
        self._manager.deviceUpdate.connect(self._onDeviceUpdate)
        self._manager.deviceDisappeared.connect(self._onDeviceDisappeared)
        self._manager.deviceCreated.connect(self._onDeviceUpdate)

        self._devices = []

        keys = {}
        keys[DeviceListModel.DEVICE_NAME_ROLE] = "deviceName"
        keys[DeviceListModel.DEVICE_ADDRESS_ROLE] = "deviceAddress"
        keys[DeviceListModel.DEVICE_PAIRED_ROLE] = "devicePaired"
        keys[DeviceListModel.DEVICE_TRUSTED_ROLE] = "deviceTrusted"
        keys[DeviceListModel.DEVICE_ICON_ROLE] = "deviceIcon"
        keys[DeviceListModel.DEVICE_BUSY_ROLE] = "deviceBusy"
        keys[DeviceListModel.DEVICE_LOW_ENERGY_ROLE] = "deviceLowEnergy"
        self.setRoleNames(keys)

    def rowCount(self, index):
        return len(self._devices)

    def getDevice(self, row):
        if row > len(self._devices):
            return None
        return self._devices[row]

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.row() > len(self._devices):
            return None

        dev = self._devices[index.row()]
        if role == DeviceListModel.DEVICE_NAME_ROLE:
            return dev.name()
        if role == DeviceListModel.DEVICE_ADDRESS_ROLE:
            return dev.address()
        elif role == DeviceListModel.DEVICE_PAIRED_ROLE:
            return dev.paired()
        elif role == DeviceListModel.DEVICE_TRUSTED_ROLE:
            return dev.trusted()
        elif role == DeviceListModel.DEVICE_ICON_ROLE:
            return dev.iconName()
        elif role == DeviceListModel.DEVICE_BUSY_ROLE:
            return dev.busy()
        elif role == DeviceListModel.DEVICE_LOW_ENERGY_ROLE:
            return dev.isLowEnergy()
        else:
            return None

    @Slot(object)
    def updateDevice(self, device):
        self._onDeviceUpdate(self, device)

    @Slot(int)
    def selectDevice(self, index):
        if index < len(self._devices):
            self.deviceSelected.emit(self._devices[index])

    def _onDeviceFound(self, device):
        size = len(self._devices)
        self.beginInsertRows(QModelIndex(), size+1, size + 2)
        self._devices.append(device)
        self.endInsertRows()

    def _onDeviceDisappeared(self, device):
        i  = self._devices.index(device)
        self.beginRemoveRows(QModelIndex(), i, i)
        self._devices.remove(device)
        self.endRemoveRows()

    def _onDeviceUpdate(self, device):
        print "Device Update"
        i  = self._devices.index(device)
        if i > -1:
            index = self.index(i, 0)
            if index.isValid():
                self.reset()
                '''
                print "Index is Valid"
                values = { DeviceListModel.DEVICE_NAME_ROLE : device.name(),
                           DeviceListModel.DEVICE_ICON_ROLE : device.iconName(),
                           DeviceListModel.DEVICE_TRUSTED_ROLE: device.trusted(),
                           DeviceListModel.DEVICE_PAIRED_ROLE: device.paired(),
                           DeviceListModel.DEVICE_BUSY_ROLE: device.busy()
                           }
                self.setItemData(index, values)
                self.submit()
                '''

    deviceSelected = Signal(object)
