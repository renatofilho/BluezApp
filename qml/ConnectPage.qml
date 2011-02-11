import Qt 4.7

Page {
    id: connectPage
    property string deviceName
    property string deviceAddress
    property string imageName
    signal cancel()

    anchors.fill: parent
    BorderImage {
         anchors.fill: parent
         border { left: 10; top: 10; right: 10; bottom: 10 }
         horizontalTileMode: BorderImage.Stretch
         verticalTileMode: BorderImage.Stretch
         source: "./icons/bg.png"
    }

    Image {
        id: deviceImage
        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: deviceNameLabel.top
            margins: 10
        }
        source: imageName
    }

    Text {
        id: deviceNameLabel
        anchors {
            horizontalCenter: deviceImage.horizontalCenter
            bottom: deviceAddressLabel.top
        }
        text: deviceName
        font {
            pixelSize: 18
            bold: true
        }
    }

    Text {
        id: deviceAddressLabel
        anchors {
            horizontalCenter: deviceImage.horizontalCenter
            bottom: label.top
            bottomMargin: 50
        }
        text: deviceAddress
        color: "gray"
    }

    Text {
        id: label
        anchors {
            topMargin: 50
            horizontalCenter: parent.horizontalCenter
            bottom: pinArea.top
        }
        font {
            bold: true
            pixelSize: 18
        }
        text: "Pin code"
    }

    FocusScope {
        id: pinArea
        width: 250
        height: 60

        anchors {
            horizontalCenter: parent.horizontalCenter
            verticalCenter: parent.verticalCenter
        }

        BorderImage {
             anchors.fill: parent
             width: parent.width; height: parent.height
             border { left: 4; top: 4; right: 4; bottom: 4 }
             source: "./icons/field.png"
        }

        TextInput {
            id: pinField
            anchors {
                fill: parent
                margins: 10
            }
            focus: true
            text: '1234'
            font.weight: Font.DemiBold
            font.pixelSize: 30
        }
    }

    Row {
        anchors {
            topMargin: 50
            top: pinArea.bottom
            horizontalCenter: parent.horizontalCenter
        }

        Rectangle {
            id: leftButton
            width: 120
            height: 60

            BorderImage {
                id: leftButtonBG
                anchors.fill: parent
                border { left: 5; top: 5; right: 5; bottom: 5 }
                source: leftArea.pressed ? './icons/btn_left_on.png' : './icons/btn_left_off.png'
            }

            Text {
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: 'Cancel'
                font.weight: Font.DemiBold
                font.pixelSize: 20
            }

            MouseArea {
                id: leftArea
                anchors.fill: parent
                onClicked: pageSlider.popPage()
            }
        }

        Rectangle {
            id: rightButton
            width: 120
            height: 60

            BorderImage {
                id: rightButtonBG
                anchors.fill: parent
                border { left: 5; top: 5; right: 5; bottom: 5 }
                source: rightArea.pressed ? './icons/btn_right_on.png' : './icons/btn_right_off.png'
            }

            Text {
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                text: 'Connect'
                font.weight: Font.DemiBold
                font.pixelSize: 20
            }

            MouseArea {
                id: rightArea
                anchors.fill: parent
                onClicked: {
                    deviceManager.connectTo(connectPage.deviceAddress, pinField.text)
                    pageSlider.popPage()
                }
            }
        }
    }
}
