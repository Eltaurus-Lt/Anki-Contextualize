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

    sentenceFields = config["fields"]["sentence"]
    if not sentenceFields:
        tooltip(f'no sentence fields specified in the config')
        return

    query = ''

    wordField = fields[MostLikely.fieldIndex(fields, "main")]
    word = note[wordField]
    if word:
        wordForms = [word]
        conj_pack = MostLikely.fieldConjugationPack(wordField)
        if conj_pack != '—':
            wordForms += [conj for wordForm in Conjugations.conjugate(word, conj_pack) for conj in wordForm["conjs"]]

        for sentenceField in sentenceFields:
            for wordForm in wordForms:
                if wordForm:
                    query += f' OR "{sentenceField}:*{wordForm}*"'
        if query.startswith(' OR '):
            query = query[4::]

    altQuery = ''

    altField = fields[MostLikely.fieldIndex(fields, "alt")]
    alt = note[altField]
    if alt:
        altForms = [alt]
        conj_pack = MostLikely.fieldConjugationPack(altField)
        if conj_pack != '—':
            altForms += [conj for altForm in Conjugations.conjugate(alt, conj_pack) for conj in altForm["conjs"]]        

        for sentenceField in sentenceFields:
            for altForm in altForms:
                if altForm:
                    altQuery += f' OR "{sentenceField}:*{altForm}*"'
        if altQuery.startswith(' OR '):
            altQuery = altQuery[4::]

    if not query:
        query = altQuery
        altQuery = ''
    if altQuery:
        query = f'({query}) OR ({altQuery})'

    AnkiBrowserSearch(query)


def setupEditorButtonsFilter(buttons, editor):

    buttons.insert(0,
        editor.addButton(
            os.path.join(addon_path, "icons", "contextSearch.svg"),
            'contextSearch',
            contextSearch,
            tip="Search for sentences containing the word"
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