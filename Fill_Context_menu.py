from . import Dialogs
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import tooltip


def fill_choices(browser):
    notes = [mw.col.get_note(note_id) for note_id in browser.selected_notes()]

    # Defining a set of all fields present in the selected notes
    all_fields = []
    for note in notes:
        all_fields += note.keys()

    added = set()
    unique_fields = [field for field in all_fields if not (field in added or added.add(field))]

    # Settings Dialog
    dialog = Dialogs.FillChoices(['—'] + unique_fields)
    if not dialog.exec():
        return
    sample_field, screen_field, source_field, source_text = dialog.get_selected_options()

    # Gathering all potential choice options
    all_choices = set()
    for note in notes:
        if source_field in note.keys():
            all_choices.add(note[source_field])

    # Filling choices field on each note
    counter = 0
    for note in notes:
        counter += 1

    tooltip(f'Choices filled for {counter} notes')
    


def choices_context_menu(browser):
    menuC = browser.form.menu_Cards
    actionC = menuC.addAction("Contextualize")
    qconnect(actionC.triggered, lambda: fill_choices(browser))

    menuN = browser.form.menu_Notes
    actionN = menuN.addAction("Contextualize")
    qconnect(actionN.triggered, lambda: fill_choices(browser))


gui_hooks.browser_menus_did_init.append(choices_context_menu)