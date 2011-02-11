import Qt 4.7

Page {
    id: page
    anchors.fill: parent
    signal deviceClicked(int id, bool devicePaired, string deviceName, string deviceAddress, bool isLowEnergy, string imageName)

    BorderImage {
         anchors.fill: parent
         border { left: 10; top: 10; right: 10; bottom: 10 }
         horizontalTileMode: BorderImage.Stretch
         verticalTileMode: BorderImage.Stretch
         source: "./icons/bg.png"
    }

    Component {
        id: deviceDelegate
        Item {
            id: row
            width: 480; height: 60
            anchors.margins: 10
            Image {
                id: icon
                anchors {
                    left: parent.left
                    top: parent.top
                    margins: 5
                }
                source: deviceIcon
            }
            Column {
                id: status
                anchors {
                    left: icon.right
                    top: parent.top
                    margins: 5
                }
                Image {
                    id: paired
                    source: devicePaired ? "./icons/paired.png" : "./icons/unpaired.png"
                }
                Image {
                    id: trusted
                    source: './icons/battery.png'
                    visible: deviceLowEnergy
                }
            }

            Text {
                id: name
                anchors {
                    left: status.right
                    verticalCenter: parent.verticalCenter
                    margins: 5
                }

                text: deviceName
                font.family: 'Verdana'
            }

            BusyIndicator {
                id: busyIndicator
                anchors {
                    right: parent.right
                    verticalCenter: parent.verticalCenter
                }
                on: deviceBusy
            }

            Image {
                id: next
                anchors.right: parent.right
                source: "./icons/next.png"
                visible: devicePaired && !busyIndicator.visible
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                onClicked: {
                    deviceListModel.selectDevice(index)
                    page.deviceClicked(index, devicePaired, deviceName, deviceAddress, deviceLowEnergy, deviceIcon)
                }
            }

            Rectangle {
                anchors {
                    margins: 5
                    top: icon.bottom
                    left : parent.left
                    right: parent.right
                }
                height: 1;
            }
        }
    }

    Text {
        width: 480
        height: 80

        id: title
        text: 'Devices'
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font {
            family: 'Verdana'
            pointSize: 24
        }
    }

    ListView {
        id: listOfDevices
        anchors {
            margins: 2
            top: title.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }
        model: deviceListModel
        delegate: deviceDelegate
    }

/*
    Rectangle {
        id: connectWindow
        width: 300
        height: 200
        opacity: 0.0
        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }
        Loader {
            source: "./connect.qml"
            visible: true
        }
    }
*/
}
