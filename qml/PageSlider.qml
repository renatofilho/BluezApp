/****************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the Qt Components project on Qt Labs.
**
** No Commercial Usage
** This file contains pre-release code and may not be distributed.
** You may use this file in accordance with the terms and conditions contained
** in the Technology Preview License Agreement accompanying this package.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPL included in the
** packaging of this file.  Please review the following information to
** ensure the GNU Lesser General Public License version 2.1 requirements
** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** If you have questions regarding the use of this file, please contact
** Nokia at qt-info@nokia.com.
**
****************************************************************************/

import Qt 4.7

import "PageSlider.js" as Core

Item {
    id: pageSlider
    property int pageCount : 0
    property Page currentPage
    property real topPageMargin : 0
    property real bottomPageMargin : 0
    property bool animating : slideAnimation.running

    clip: true

    Flickable {
        id: flickable
        interactive: false
        anchors.fill: parent
        contentWidth: content.width
        contentHeight: content.height

        property bool sliding : false
        contentX: Math.max(0, pageCount - 1) * flickable.width

        Row {
            id: content
        }

        Behavior on contentX {
            enabled: flickable.sliding

            SequentialAnimation {
                id: slideAnimation
                NumberAnimation {
                    duration: 400
                }
                ScriptAction {
                    script: Core.finalize();
                }
            }
        }
    }

    Component {
        id: pageContainer
        Item {
            width: flickable.width
            height: flickable.height

            property Page page
            property alias viewport : pageContainerViewport

            Item {
                id: pageContainerViewport
                anchors.fill: parent
                anchors.topMargin: topPageMargin
                anchors.bottomMargin: bottomPageMargin
            }
        }
    }

    function pushPage(component) {
        return Core.push(component);
    }

    function popPage() {
        return Core.pop();
    }
}
