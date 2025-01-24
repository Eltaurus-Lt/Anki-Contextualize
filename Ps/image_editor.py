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