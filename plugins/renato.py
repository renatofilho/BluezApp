class RenatoPlugin(object):

    def getName(self):
        return 'Renato'

    def getDescription(self):
        return 'Plugin do Renato'

    def getWidget(self):
        return None

    def implementedServices(self):
        return ['00000002-0000-1000-8000-0002ee000002',
                '00001000-0000-1000-8000-00805f9b34fb',
                '00001103-0000-1000-8000-00805f9b34fb']

    def getUiFile(self):
        return '../plugins/renato.qml'

    def supportService(self, service):
        return service in self.implementedServices()

    name = property(getName)
    description = property(getDescription)
    widget = property(getWidget)
    uiFile = property(getUiFile)
    services = property(implementedServices)


def register():
    return RenatoPlugin()
