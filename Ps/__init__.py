import os
from anki.hooks import addHook
from aqt import mw

addon_path = os.path.dirname(__file__)

image_field = ""

def images_from_field(field, note):
    imgs = note[field].split("<img")[1:]
    imgs = [img.split(">")[0] for img in imgs]
    imgs = [img.split("src=")[1] for img in imgs]
    imgs = [img.split('"')[1] for img in imgs]

    for img in imgs:
        os.popen(f'photoshop -o {os.path.join(mw.col.media.dir(), img)}')

def edit_in_ps(editor):
    note = editor.note
    if image_field:
        images_from_field(image_field, note)
    else:
        for field in note.keys():
            images_from_field(field, note)
    

def setupEditorButtonsFilter(buttons, editor):
    if image_field:
        tip = 'Edit {{' + image_field + '}} in Photoshop'
    else:
        tip = 'Edit all images in Photoshop'

    buttons.insert(0,
        editor.addButton(
            os.path.join(addon_path, "icons", "ps.svg"),
            'Ps',
            edit_in_ps,
            tip=tip
        )
    )

    return buttons

addHook("setupEditorButtons", setupEditorButtonsFilter)
# gui_hooks.editor_did_init_buttons.append(setupEditorButtonsFilter)