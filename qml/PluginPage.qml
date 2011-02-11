import Qt 4.7

Page {
    id: plugin
    property alias source: pluginLoader.source
    Loader {
        id: pluginLoader
    }
}

