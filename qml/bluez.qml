import Qt 4.7

Item {
    width: 480
    height: 800
    property Item devicePage
    property Item servicePage
    property Item connectionPage
    property Item pluginPage

    PageSlider
    {
       id: pageSlider
       anchors.fill: parent
    }

    Component {
        id: deviceComponent
        DeviceList { }
    }

    Component {
        id: serviceComponent
        ServiceList { }
    }

    Component {
        id: connectComponent
        ConnectPage { }
    }

    Component {
        id: pluginComponent
        PluginPage { }
    }

    Component.onCompleted: {
       devicePage = pageSlider.pushPage(deviceComponent)
    }


    Connections {
       target: devicePage
       onDeviceClicked: {
           console.log("is LowEnergy:", isLowEnergy)
           if (!devicePaired) {
               console.log("Not paired")
               if (isLowEnergy) {
                   console.log("Will connect")
                   deviceManager.connectTo(deviceAddress, '')
                } else {
                    connectionPage = pageSlider.pushPage(connectComponent)
                    connectionPage.deviceName = deviceName
                    connectionPage.deviceAddress = deviceAddress
                    connectionPage.imageName = imageName
                }
           } else {
                servicePage = pageSlider.pushPage(serviceComponent)
           }
       }
    }

    Connections {
        target: servicePage
        onServiceClicked: {
            console.log('load plugin:' + uiFile)
            pluginPage = pageSlider.pushPage(pluginComponent)
            pluginPage.source = uiFile
        }
    }
}
