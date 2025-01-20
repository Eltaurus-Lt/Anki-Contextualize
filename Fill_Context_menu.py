from . import Dialogs, Screenshots, Timestamps, Subtitles, Conjugations
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.progress import ProgressManager
from aqt.utils import tooltip
import os, re

def subtitleWordSearch(word, sentence_db):
    for entry in sentence_db:
        if word in entry['sentence']:
            return {'t1': entry['t1'], 't2': entry['t2'], 'sentence': entry['sentence'], 'word_form': word}

    return {}

def subtitleConjugatedSearch(word, sentence_db, conj_pack, pos = ""):
    # dict form
    searchResult = subtitleWordSearch(word, sentence_db)
    if searchResult:
        return searchResult

    # conj forms
    if conj_pack == '—' or not bool(conj_pack):
        return {}

    # blind match
    wordForms = Conjugations.conjugate(word, conj_pack) # add pos here if not empty for non-blind
    for wordForm in wordForms:
        for conj in wordForm['conjs']:
            searchResult = subtitleWordSearch(conj, sentence_db)
            if searchResult:
                return searchResult

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
    word_field, alts_field, conj_pack, sentence_field, screenshot_field, source_field, source_text, videoFile_path, subtitleFile_path = dialog.get_selected_options()

    sentence_db = Subtitles.parse(subtitleFile_path)
    # tooltip(sentence_db)

    screenshots_meta = set()
    progress_manager = ProgressManager(mw)
    # progress_manager.start(label = "Filling-in Notes", max = len(notes), immediate = True)
    counter = 0
    for note_n, note in enumerate(notes):
        # Source field
        if source_field in note.keys() and source_field != '—':
            note[source_field] = source_text
            mw.col.update_note(note)

        # Search
        searchResult = {}
        ## based on predefined sentence or word-form
        if sentence_field in note.keys() and sentence_field != '—' and bool(note[sentence_field]):
            searchResult = subtitleWordSearch(note[sentence_field], sentence_db)
        ## based on the main word field
        if not searchResult:
            searchResult = subtitleConjugatedSearch(note[word_field], sentence_db, conj_pack)
        ## based on the alts
        if not searchResult and alts_field != '—' and bool(note[alts_field]):
            alts = [alt.strip() for alt in re.split(r'[|｜]', note[alts_field])]
            for alt in alts:
                searchResult = subtitleConjugatedSearch(alt, sentence_db, conj_pack)
                if searchResult:
                    break
        # progress_manager.update(label = "Filling-in Notes", value = note_n)
        if not searchResult:
            continue

        # Filling-in context fields
        if sentence_field in note.keys() and sentence_field != '—':
            note[sentence_field] = formatSampleSentence(searchResult['word_form'], searchResult['sentence'])
        if screenshot_field in note.keys() and bool(videoFile_path) and screenshot_field != '—':
            ts = Timestamps.average(searchResult['t1'], searchResult['t2'])
            screenshotFilename = Screenshots.composeName(videoFile_path, ts)
            screenshots_meta.add((('ts', ts), ('filename', screenshotFilename)))
            note[screenshot_field] = f"<img src='{screenshotFilename}'/>"

        counter += 1
        mw.col.update_note(note)
        # if len(notes) == 1:
            # editor.set_note(editor.note) #refresh editor view

    progress_manager.start(label = "Making screenshots", max = len(screenshots_meta), immediate = True)

    # Make screenshot files
    for scr_n, meta in enumerate(screenshots_meta):
        meta_dict = dict(meta)
        Screenshots.save(meta_dict['ts'], meta_dict['filename'], videoFile_path)    
        progress_manager.update(value = scr_n)

    progress_manager.finish();

def choices_context_menu(browser):
    menuC = browser.form.menu_Cards
    actionC = menuC.addAction("Contextualize")
    qconnect(actionC.triggered, lambda: contextualize(browser))

    menuN = browser.form.menu_Notes
    actionN = menuN.addAction("Contextualize")
    qconnect(actionN.triggered, lambda: contextualize(browser))


gui_hooks.browser_menus_did_init.append(choices_context_menu)
