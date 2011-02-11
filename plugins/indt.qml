import Qt 4.7

Rectangle {
    BorderImage {
         anchors.fill: parent
         border { left: 10; top: 10; right: 10; bottom: 10 }
         horizontalTileMode: BorderImage.Stretch
         verticalTileMode: BorderImage.Stretch
         source: "../qml/icons/bg.png"
    }

    Text {
        anchors.fill: parent
        text: 'Plugin do INdT'
    }
}
