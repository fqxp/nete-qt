/****************************************************************************
**
**
** Copyright (c) 2014 Ricardo do Valle Flores de Oliveira
**
** $BEGIN_LICENSE:MIT$
** Permission is hereby granted, free of charge, to any person obtaining a copy
** of this software and associated documentation files (the "Software"), to deal
** in the Software without restriction, including without limitation the rights
** to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
** copies of the Software, and to permit persons to whom the Software is
** furnished to do so, subject to the following conditions:
**
** The above copyright notice and this permission notice shall be included in
** all copies or substantial portions of the Software.
**
** THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
** IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
** FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
** AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
** LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
** OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
** SOFTWARE.
**
**
****************************************************************************/

import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Button {
    id: button
    property string icon
    property font font
    property bool enabled: false

    style: ButtonStyle {
        id: buttonstyle
        property font font: button.font
        property color foregroundColor: "black"
        property color backgroundColor: "white"
        property color enabledForegroundColor: "white"
        property color enabledBackgroundColor: "#888888"
        property color hoverColor: "#eeeeee"
        property color enabledHoverColor: "#aaaaaa"

        background: Item {
            Rectangle {
                id: baserect
                anchors.fill: parent
                color: button.hovered ?
                    (button.enabled ? enabledHoverColor : hoverColor)
                    : (button.enabled ? enabledBackgroundColor : backgroundColor)
            }
        }

        label: Item {
            anchors.centerIn: parent
            Text {
                id: iconLabel
                color: button.enabled ? buttonstyle.enabledForegroundColor : buttonstyle.foregroundColor
                font {
                    pointSize: buttonstyle.font.pointSize
                    family: awesome.family
                }
                text: icon
                visible: !(icon === "")
                anchors {
                    right: textLabel.visible ? textLabel.left : undefined;
                    rightMargin: textLabel.visible ? control.font.pointSize / 2 : undefined;
                    centerIn: textLabel.visible ? null : parent;
                    verticalCenter: textLabel.verticalCenter
                }
            }

            Text {
                id: textLabel
                color: button.enabled ? buttonstyle.enabledForegroundColor : buttonstyle.foregroundColor
                font: buttonstyle.font
                renderType: Text.NativeRendering
                text: control.text
                visible: !(control.text === "")
                anchors.centerIn: parent
            }
        }
    }
}
