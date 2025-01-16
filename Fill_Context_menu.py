from . import Dialogs, Screenshots, Timestamps, Subtitles
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.utils import tooltip
import os

def wordConjugations(word, word_alts, pos, dic):
    # generate possible word forms based on part of speech (pos) and rules from referenced dictionary file
    # append (overwrite with?) word_alts if not empty
    return {word}

def subtitleWordSearch(word_forms, sentence_db):
    for entry in sentence_db:
        for word in word_forms:
            if word in entry['sentence']:
                return {'t1': entry['t1'], 't2': entry['t2'], 'sentence': entry['sentence'], 'word_form': word}

    return {}

def formatSampleSentence(word_form, sentence):
    return sentence

def contextualize(browser):
    notes = [mw.col.get_note(note_id) for note_id in browser.selected_notes()]

    # Defining a set of all fields present in the selected notes
    unique_fields = []
    added = set()
    for note in notes:
        for field in note.keys():
            if not (field in added or added.add(field)):
                unique_fields.append(field)

    # Settings Dialog
    dialog = Dialogs.FillContext(unique_fields)
    if not dialog.exec():
        return
    word_field, word_conj_field, sentence_field, screenshot_field, source_field, source_text, videoFile_path, subtitleFile_path = dialog.get_selected_options()
    # tooltip(f'{sentence_field}, {screenshot_field}, {source_field}, {source_text}, {videoFile_path}, {subtitleFile_path}')

    sentence_db = Subtitles.parse(subtitleFile_path)
    # tooltip(sentence_db)

    screenshots_meta = set()
    counter = 0
    for note in notes:

        # Search
        searchResult = {}
        if sentence_field in note.keys() and sentence_field != '—' and bool(note[sentence_field]):
            searchResult = subtitleWordSearch({note[sentence_field]}, sentence_db)
        if not searchResult:
            word_conjugations = {note[word_field]} # wordConjugations(note[word_field], note[word_conj_field], "", "")
            searchResult = subtitleWordSearch(word_conjugations, sentence_db)   
        if not searchResult:
            continue

        # Field contents
        if sentence_field in note.keys() and sentence_field != '—':
            note[sentence_field] = formatSampleSentence(searchResult['word_form'], searchResult['sentence'])
        if bool(videoFile_path) and screenshot_field in note.keys() and screenshot_field != '—':
            ts = Timestamps.average(searchResult['t1'], searchResult['t2'])
            screenshotFilename = Screenshots.composeName(videoFile_path, ts)
            screenshots_meta.add((('ts', ts), ('filename', screenshotFilename)))
            note[screenshot_field] = f"<img src='{screenshotFilename}'/>"
        if source_field in note.keys() and source_field != '—':
            note[source_field] = source_text

        counter += 1
        mw.col.update_note(note)
        # if len(notes) == 1:
            # editor.set_note(editor.note) #refresh editor view


    # Make screenshot files
    for meta in screenshots_meta:
        meta_dict = dict(meta)
        Screenshots.save(meta_dict['ts'], meta_dict['filename'], videoFile_path)    


def choices_context_menu(browser):
    menuC = browser.form.menu_Cards
    actionC = menuC.addAction("Contextualize")
    qconnect(actionC.triggered, lambda: contextualize(browser))

    menuN = browser.form.menu_Notes
    actionN = menuN.addAction("Contextualize")
    qconnect(actionN.triggered, lambda: contextualize(browser))


gui_hooks.browser_menus_did_init.append(choices_context_menu)
