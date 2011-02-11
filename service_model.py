from PySide.QtCore import QAbstractListModel, Qt, QModelIndex
from pluginloader import BluezPluginLoader


class ServiceListModel(QAbstractListModel):
    SERVICE_NAME_ROLE = Qt.UserRole + 1
    SERVICE_DESCRIPTION_ROLE = SERVICE_NAME_ROLE + 1
    SERVICE_UI_FILE_ROLE = SERVICE_NAME_ROLE + 3
    SERVICE_HAS_DETAILS_ROLE = SERVICE_NAME_ROLE + 4

    def __init__(self, parent=None):
        super(ServiceListModel, self).__init__(parent)
        self._device = None
        self._servicesId = []
        self._servicesPlugins = []
        self._pluginLoader = BluezPluginLoader()

        keys = {}
        keys[ServiceListModel.SERVICE_NAME_ROLE] = "serviceName"
        keys[ServiceListModel.SERVICE_DESCRIPTION_ROLE] = "serviceDescription"
        keys[ServiceListModel.SERVICE_UI_FILE_ROLE] = "serviceUiFile"
        keys[ServiceListModel.SERVICE_HAS_DETAILS_ROLE] = "serviceHasDetails"

        self.setRoleNames(keys)

    def rowCount(self, index):
        return len(self._servicesPlugins)

    def data(self, index, role):
        if not index.isValid():
            print "invalid"
            return None

        if index.row() > len(self._servicesPlugins):
            return None

        service = self._servicesPlugins[index.row()]
        if role == ServiceListModel.SERVICE_NAME_ROLE:
            return service.name
        elif role == ServiceListModel.SERVICE_DESCRIPTION_ROLE:
            return service.description
        elif role == ServiceListModel.SERVICE_UI_FILE_ROLE:
            return service.uiFile
        elif role == ServiceListModel.SERVICE_HAS_DETAILS_ROLE:
            return len(service.uiFile) > 0
        else:
            return None

    def loadDevice(self, device):
        if self._device and self._device == device:
            return

        self._device = device
        self.beginRemoveRows(QModelIndex(), 0, len(self._servicesPlugins))
        self._servicesPlugins = []
        self.endRemoveRows()

        newServices = device.getServices()
        (plugins, ids) = self._pluginLoader.getPlugins(newServices)
        if len(ids):
            print "================================================"
            print "Not supported services"
            print "================================================"
            for name in ids:
                print "Not supported services", str(name)
            print "================================================"
        size = len(plugins)
        self.beginInsertRows(QModelIndex(), 0, size)
        self._servicesPlugins = plugins
        self.endInsertRows()
