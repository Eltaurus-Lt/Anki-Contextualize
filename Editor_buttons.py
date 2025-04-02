import os
from aqt import dialogs, mw
from aqt.utils import tooltip
from anki.hooks import addHook
from . import Conjugations, MostLikely

addon_path = os.path.dirname(__file__)
config = mw.addonManager.getConfig(__name__)

def AnkiBrowserSearch(query):
    if not query:
        return False
    if not mw.col.find_notes(query):
        tooltip(f'no notes found')
        return
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(query)
    browser.onSearchActivated()
    return True
	

def contextSearch(editor):
    note = editor.note
    fields = note.keys()

    wordField = fields[MostLikely.fieldIndex(fields, "main")]
    word = note[wordField]

    sentenceFields = config["fields"]["sentence"]
    if not sentenceFields:
        tooltip(f'no sentence fields specified in the config')
        return

    wordForms = [word]
    conj_pack = MostLikely.fieldConjugationPack(wordField)
    if conj_pack != '—':
        wordForms += [conj for wordForm in Conjugations.conjugate(word, conj_pack) for conj in wordForm["conjs"]]

    query = ''
    for sentenceField in sentenceFields:
    	for wordForm in wordForms:
    		query += f' OR "{sentenceField}:*{wordForm}*"'
    if query.startswith(' OR '):
        query = query[4::]

# altField = fields[MostLikely.fieldIndex(fields, "alt")]

    AnkiBrowserSearch(query)


def setupEditorButtonsFilter(buttons, editor):

    buttons.insert(0,
        editor.addButton(
            os.path.join(addon_path, "icons", "contextSearch.svg"),
            'contextSearch',
            contextSearch,
            tip="Search for other sentences containing the word"
        )
    )
    # buttons.insert(0,
    #     editor.addButton(
    #         os.path.join(addon_path, "icons", "edupl.svg"),
    #         'ImageDuplicates',
    #         image_duplicates,
    #         tip="Find notes with same images"
    #     )
    # )
    # buttons.insert(2,
    #     editor.addButton(
    #         os.path.join(addon_path, "icons", "highlight.svg"),
    #         'wordHighlight',
    #         wordHighlight,
    #         tip="(Auto)highlight the word in the text sample"
    #     )
    # )

    return buttons

addHook("setupEditorButtons", setupEditorButtonsFilter)