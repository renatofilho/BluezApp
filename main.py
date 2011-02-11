from PySide.QtCore import QUrl
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView
import sys

from device_model import DeviceListModel
from service_model import ServiceListModel
from device_manager import DeviceManager

if __name__ == '__main__':
    QApplication.setGraphicsSystem("raster")
    app = QApplication(sys.argv)

    view = QDeclarativeView()
    engine = view.engine()
    engine.quit.connect(app.quit)

    if len(sys.argv) > 1:
        manager = DeviceManager(sys.argv[1])
    else:
        manager = DeviceManager()

    deviceListModel = DeviceListModel(manager)
    serviceListModel = ServiceListModel()
    deviceListModel.deviceSelected.connect(serviceListModel.loadDevice)

    view.rootContext().setContextProperty("deviceManager", manager)
    view.rootContext().setContextProperty("deviceListModel", deviceListModel)
    view.rootContext().setContextProperty("serviceListModel", serviceListModel)

    context = view.rootContext()

    view.setSource(QUrl('./qml/bluez.qml'))
    view.setMinimumSize(480, 800)
    view.show()

    manager.start()
    sys.exit(app.exec_())

