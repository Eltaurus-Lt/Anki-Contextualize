from . import Dialogs
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import tooltip

def subtitleParse(filepath):
    return [{'ts': 42, 'sentence': "ピクニックに行く"}]

def wordConjugations(word, word_alts, pos, dic):
    # generate possible word forms based on part of speech (pos) and rules from referenced dictionary file
    # append (overwrite with?) word_alts if not empty
    return {word}

def subtitleWordSearch(word_forms, sentence_db):
    return {'ts': 42, 'sentence': "ピクニックに行く", 'word_form': "行く"}

def formatSampleSentence(word_form, sentence):
    return sentence

def composeScreenshotFilename(source_filename, t):
    return "screenshot00.png"

def saveScreenshot(ts, saveas, videoSource):
    return

def contextualize(browser):
    notes = [mw.col.get_note(note_id) for note_id in browser.selected_notes()]

    # Defining a set of all fields present in the selected notes
    all_fields = []
    for note in notes:
        all_fields += note.keys()

#optimize by moving the filter into the loop above
    added = set()
    unique_fields = [field for field in all_fields if not (field in added or added.add(field))]

    # Settings Dialog
    dialog = Dialogs.FillChoices(['—'] + unique_fields)
    if not dialog.exec():
        return
    word_field, word_conj_field, sentence_field, screenshot_field, source_field, source_text, videoFile_path, subtitleFile_path = dialog.get_selected_options()

    sentence_db = subtitleParse(subtitleFile_path)

    screenshots_meta = set()
    counter = 0
    for note in notes:
# add checks for non-existing fields and empty search results
        word_conjugations = wordConjugations(note[word_field], note[word_conj_field], "", "")
        searchResult = subtitleWordSearch(word_conjugations, sentence_db)
        note[sentence_field] = formatSampleSentence(searchResult['word_form'], searchResult['sentence'])
        screenshotFilename = composeScreenshotFilename(videoFile_path, searchResult['ts'])
        screenshots_meta.add({'ts': searchResult['ts'], 'filename': screenshotFilename})
        note[screenshot_field] = f"<img src='{screenshotFilename}'/>"
        note[source_field] = source_text
        counter += 1
#<- save note

    # Make screenshots
    for meta in screenshots_meta:
        saveScreenshot(meta['ts'], meta['filename'], videoFile_path)

    tooltip(f'{sample_field}, {screenshot_field}, {source_field}, {source_text}, {videoFile_path}, {subtitleFile_path}')
    


def choices_context_menu(browser):
    menuC = browser.form.menu_Cards
    actionC = menuC.addAction("Contextualize")
    qconnect(actionC.triggered, lambda: contextualize(browser))

    menuN = browser.form.menu_Notes
    actionN = menuN.addAction("Contextualize")
    qconnect(actionN.triggered, lambda: contextualize(browser))


gui_hooks.browser_menus_did_init.append(choices_context_menu)