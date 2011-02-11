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

var items = [];
var pendingItems = [];

function push(component)
{
    var item = pageContainer.createObject(content);
    if (item == null)
        return null;

    var page = component.createObject(item.viewport);
    if (page == null) {
        item.destroy();
        return null;
    }

    item.page = page;
    items.push(item);
    update();

    return page;
}

function pop()
{
    if (items.length == 0)
        return false;

    var item = items.pop();
    item.page.aboutToExit();
    pendingItems.push(item);
    update();

    return true;
}

function update()
{
    var index = items.length - 1;

    if (index >= 0) {
        var page = items[index].page;
        page.visible = true;
        pageSlider.currentPage = page;
    } else {
        pageSlider.currentPage = null;
    }

    flickable.sliding = true;
    pageSlider.pageCount = items.length;
}

function finalize()
{
    for (var i = 0; i < items.length; i++) {
        var isCurrent = (i == items.length - 1);
        if (isCurrent)
            items[i].page.entered();
        items[i].page.visible = isCurrent;
    }

    while (pendingItems.length > 0) {
        var item = pendingItems.pop();
        item.destroy();
    }

    flickable.sliding = false;
}
