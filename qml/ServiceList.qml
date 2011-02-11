import Qt 4.7

Page {
    id: servicePage
    anchors.fill: parent
    signal serviceClicked(string name, string uiFile)

    BorderImage {
         anchors.fill: parent
         border { left: 10; top: 10; right: 10; bottom: 10 }
         horizontalTileMode: BorderImage.Stretch
         verticalTileMode: BorderImage.Stretch
         source: "./icons/bg.png"
    }

    Component {
        id: serviceDelegate
        Item {
            id: row
            width: 480; height: 60
            anchors.margins: 10
            Text {
                id: name
                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                    margins: 10
                }
                text: serviceName
            }

            Text {
                id: description
                anchors {
                    top: name.bottom
                    left: parent.left
                    right: parent.right
                    leftMargin: 10
                }

                text: serviceDescription
                color: 'gray'
            }

            Image {
                id: next
                anchors.right: parent.right
                source: "./icons/next.png"
                visible: serviceHasDetails
            }

            Rectangle {
                anchors {
                    margins: 5
                    top: description.bottom
                    left : parent.left
                    right: parent.right
                }
                height: 1;
            }

            MouseArea {
                id: mouseArea
                anchors.fill: parent
                onClicked: {
                    if (serviceHasDetails) {
                        servicePage.serviceClicked(serviceName, serviceUiFile)
                    }
                }
            }

        }
    }

    Text {
        width: 480
        height: 80

        id: title
        text: 'Services'
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font {
            family: 'Verdana'
            pointSize: 24
        }
    }


    ListView {
        id: listofServices
        anchors {
            margins: 2
            top: title.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        model: serviceListModel
        delegate: serviceDelegate
    }
}
