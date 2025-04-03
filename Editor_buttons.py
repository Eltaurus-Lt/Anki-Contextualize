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


def closingTag(tag):
    if '<' not in tag:
        if '>' in tag:
            return "error"
        else:
            return ''

    tag = tag[tag.index('<') + 1::]

    # todo: check if tag is img (or other self-closing) and crop till the next tag / multiple closing tags

    if '>' not in tag:
        return "error"

    for ed in [' ', '>']:
        if ed in tag:
            tag = tag[:tag.index(ed)]

    if tag.startswith('/'):
        return "error"

    return "</" + tag + ">"


def wordHighlightLegacy(editor):
    OP = config["highlight"]["tag"]
    ED = closingTag(OP)
    if ED and '>' not in ED:
        tooltip('incorrect highlight tag, check the config')
        return

    selection = editor.web.selectedText()
    if not selection:
        return

    editor.web.eval(f"document.execCommand('insertHTML', false, {repr(OP + selection + ED)});")


def updIconHighlightColor(icon_file):
    svg_path = os.path.join(addon_path, "icons", f"{icon_file}")

    if os.path.exists(svg_path):
        with open(svg_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

    for i, line in enumerate(lines):
        if "--col-highlight:" in line:
            lines[i] = f'--col-highlight: {config["highlight"]["color"]};\n'
        
    with open(svg_path, "w", encoding="utf-8") as file:
        file.writelines(lines)


def setupEditorButtonsFilter(buttons, editor):

    #modify highlight color in the button icons
    icon_folder = os.path.join(addon_path, "icons")
    [updIconHighlightColor(f) for f in os.listdir(icon_folder) if os.path.isfile(os.path.join(icon_folder, f))]



    buttons.insert(0,
        editor.addButton(
            os.path.join(addon_path, "icons", "contextSearch.svg"),
            'contextSearch',
            contextSearch,
            tip="Search for sentences containing the word"
        )
    )
    buttons.insert(1,
        editor.addButton(
            os.path.join(addon_path, "icons", "highlight.svg"),
            'wordHighlight',
            wordHighlightLegacy,
            tip="(Auto)highlight the word in the text sample"
        )
    )
    # buttons.insert(0,
    #     editor.addButton(
    #         os.path.join(addon_path, "icons", "edupl.svg"),
    #         'ImageDuplicates',
    #         image_duplicates,
    #         tip="Find notes referencing same images"
    #     )
    # )


    return buttons



addHook("setupEditorButtons", setupEditorButtonsFilter)