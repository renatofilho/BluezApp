class RenatoPlugin(object):

    def getName(self):
        return 'INdT'

    def getDescription(self):
        return 'Plugin do INdT'

    def getWidget(self):
        return None

    def implementedServices(self):
        return ['00001112-0000-1000-8000-00805f9b34fb',
                '00001000-0000-1000-8000-00805f9b34fb',
                '00001200-0000-1000-8000-00805f9b34fb',
                '00005005-0000-1000-8000-0002ee000001']

    def getUiFile(self):
        return '../plugins/indt.qml'

    def supportService(self, service):
        return service in self.implementedServices()

    name = property(getName)
    description = property(getDescription)
    widget = property(getWidget)
    uiFile = property(getUiFile)
    services = property(implementedServices)


def register():
    return RenatoPlugin()
