import os
from anki.hooks import addHook
# from aqt import gui_hooks

from aqt.utils import tooltip

addon_path = os.path.dirname(__file__)

def onclick(editor):
    tooltip('the Button is pressed')    

def setupEditorButtonsFilter(buttons, editor):
    buttons.insert(0,
        editor.addButton(
            os.path.join(addon_path, "icons", "button.svg"),
            'Button',
            onclick,
            tip="text description"
        )
    )

    return buttons
    

addHook("setupEditorButtons", setupEditorButtonsFilter)
# gui_hooks.editor_did_init_buttons.append(setupEditorButtonsFilter)