from anki.hooks import addHook
from . import image_editor

addHook("setupEditorButtons", image_editor.setupEditorButtonsFilter)
# gui_hooks.editor_did_init_buttons.append(setupEditorButtonsFilter)