import os
import imp
import sys

class BluezPluginLoader(object):
    def __init__(self):
        pluginpath = os.path.join(os.path.dirname(imp.find_module("pluginloader")[1]), "plugins/")
        pluginfiles = [fname[:-3] for fname in os.listdir(pluginpath) if fname.endswith(".py")]
        if not pluginpath in sys.path:
            sys.path.append(pluginpath)
        imported_modules = [__import__(fname) for fname in pluginfiles]

        self._plugins = []

        for mod in imported_modules:
            self._plugins.append(mod.register())


    def getPlugins(self, services):
        plugins = []
        for service in services:
            for p in self._plugins:
                if p.supportService(service) and p not in plugins:
                    plugins.append(p)
                    services.remove(service)

        return (plugins, services)
