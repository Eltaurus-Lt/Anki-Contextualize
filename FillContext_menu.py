# This script is part of the Contextualize Add-on for Anki.
# Source: https://github.com/Eltaurus-Lt/Anki-Contextualize
# 
# Copyright © 2024-2025 Eltaurus and zunios
# Contact: 
#     Email: Eltaurus@inbox.lt
#     GitHub: github.com/Eltaurus-Lt, https://github.com/zunios
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

from . import Dialogs, Screenshots, Timestamps, Subtitles, SubtitleSearch, MostLikely
from aqt import mw, gui_hooks
from aqt.qt import qconnect
from aqt.progress import ProgressManager
from aqt.utils import tooltip
import os, re

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
    (
        word_field, alts_field, conj_pack, 
        sentence_field, screenshot_field, source_field, 
        videoFile_path, subtitleFile_path, source_text, tag_string
    ) = dialog.get_selected_options()

    try:
        sentence_db = Subtitles.parse(subtitleFile_path)
        if not sentence_db:
            tooltip("❌ Parsing the subtitle file did not return any results")
            return
    except Exception as error:
        tooltip(f"❌ {error}")
        return


    try:
        makeScreenshots = (screenshot_field != '—' and Screenshots.enabled(videoFile_path))
    except Exception as error:
        tooltip(f"⚠️ Screenshots cannot be taken ({error})")
        makeScreenshots = False

    screenshots_meta = set()
    progress_manager = ProgressManager(mw)
    # progress_manager.start(label = "Filling-in Notes", max = len(notes), immediate = True)
    log = []
    for note_n, note in enumerate(notes):

        # Search
        searchResult = {}
        ## based on the predefined sentence or word-form
        if sentence_field in note.keys() and note[sentence_field]:
            searchResult = SubtitleSearch.searchExact(note[sentence_field], sentence_db)
        ## based on the main word field
        if not searchResult:
            searchResult = SubtitleSearch.searchConjugated(note[word_field], sentence_db, conj_pack)
        ## based on the alts
        if not searchResult and alts_field in note.keys() and note[alts_field]:
            alts = re.split(r'[|｜]', note[alts_field])
            for alt in alts:
                searchResult = SubtitleSearch.searchConjugated(alt, sentence_db, conj_pack)
                if searchResult:
                    break
        # progress_manager.update(label = "Filling-in Notes", value = note_n)

        log_wordForm = note[word_field]
        if not log_wordForm and alts_field in note.keys():
            log_wordForm = note[alts_field]

        if not log_wordForm and sentence_field in note.keys():
            log_wordForm = note[sentence_field]

        if not searchResult:
            log.append((log_wordForm, ""))
            continue



        # Filling-in context fields

        if sentence_field in note.keys():
            note[sentence_field] = formatSampleSentence(searchResult['word_form'], searchResult['sentence'])
            log.append((log_wordForm, note[sentence_field]))
        else:
            log.append((log_wordForm, "✅"))

        if screenshot_field in note.keys() and makeScreenshots:
            ts = Timestamps.average(searchResult['t1'], searchResult['t2'])
            screenshotFilename = Screenshots.composeName(videoFile_path, ts)
            screenshots_meta.add((('ts', ts), ('filename', screenshotFilename)))
            note[screenshot_field] = f"<img src='{screenshotFilename}'/>"

        if source_field in note.keys():
            note[source_field] = source_text
        # adding tags
        tags = {tag.strip() for tag in re.split(r'[ \u3000]', tag_string)}
        for tag in tags:
            if bool(tag):
                note.add_tag(tag)

        mw.col.update_note(note)



    progress_manager.start(label = "Making screenshots", max = len(screenshots_meta), immediate = True)

    # Make screenshot files
    for scr_n, meta in enumerate(screenshots_meta):
        meta_dict = dict(meta)
        Screenshots.save(meta_dict['ts'], meta_dict['filename'], videoFile_path)    
        progress_manager.update(value = scr_n)

    progress_manager.finish()

    if len(notes) == 1:
        editor = MostLikely.editor(notes[0].id)
        if editor:
            editor.setNote(mw.col.get_note(notes[0].id)) #refresh editor view
    else:
        Dialogs.ResultsLog(log).exec()



def choices_context_menu(browser):
    menuC = browser.form.menu_Cards
    actionC = menuC.addAction("Contextualize")
    qconnect(actionC.triggered, lambda: contextualize(browser))

    menuN = browser.form.menu_Notes
    actionN = menuN.addAction("Contextualize")
    qconnect(actionN.triggered, lambda: contextualize(browser))


gui_hooks.browser_menus_did_init.append(choices_context_menu)
