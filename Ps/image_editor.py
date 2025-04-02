# This script is part of the Contextualize Add-on for Anki.
# Source: https://github.com/Eltaurus-Lt/Anki-Contextualize
# 
# Copyright © 2024-2025 Eltaurus
# Contact: 
#     Email: Eltaurus@inbox.lt
#     GitHub: github.com/Eltaurus-Lt
#     Anki Forums: forums.ankiweb.net/u/Eltaurus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os
from aqt import mw

config = mw.addonManager.getConfig(__name__)

image_field = ""

editors = ["Photoshop", "GIMP", "Krita"]

def imageEditorQ():
    for editor in editors:
        if editor.lower() in config["image editor path"].lower():
            return editor    
    return "Image Editor"

def images_from_field(field, note):
    imgs = note[field].split("<img")[1:]
    imgs = [img.split(">")[0] for img in imgs]
    imgs = [img.split("src=")[1] for img in imgs]
    imgs = [img.split('"')[1] for img in imgs]

    for img in imgs:
        os.popen(f'{config["image editor path"]} {os.path.join(mw.col.media.dir(), img)}')

def edit_image(editor):
    note = editor.note
    if image_field:
        images_from_field(image_field, note)
    else:
        for field in note.keys():
            images_from_field(field, note)
    

def setupEditorButtonsFilter(buttons, editor):
    if image_field:
        tip = 'Edit {{' + image_field + '}} in ' + imageEditorQ()
    else:
        tip = 'Edit all images in ' + imageEditorQ()

    buttons.insert(0,
        editor.addButton(
            os.path.join(os.path.dirname(__file__), "..", "icons", "ps.svg"),
            'Ps',
            edit_image,
            tip=tip
        )
    )

    return buttons