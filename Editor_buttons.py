# This script is part of the Contextualize Add-on for Anki.
# Source: https://github.com/Eltaurus-Lt/Anki-Contextualize
# 
# Copyright © 2024-2025 Eltaurus
# Contact: 
#     Email: Eltaurus@inbox.lt
#     GitHub: github.com/Eltaurus-Lt
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

import os, json
from aqt import dialogs, mw, gui_hooks
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

def wordHighlightAuto(editor, OP, ED):
    note = editor.note
    fields = note.keys()

    wordField = fields[MostLikely.fieldIndex(fields, "main")]
    word = note[wordField]
    altField = fields[MostLikely.fieldIndex(fields, "alt")]
    alt = note[altField]
    if not word and not alt:
        tooltip(f'no text selected in the editor and both {wordField} and {altField} are empty')
        return

    sentenceFieldCandidates = config["fields"]["sentence"]
    if not sentenceFieldCandidates:
        tooltip(f'no text selected in the editor and sentence fields specified in the config')
        return

    sentenceIndex = MostLikely.fieldIndex(['—'] + fields, "sentence")
    if sentenceIndex == 0:
        tooltip(f'no text selected in the editor and no sentence fields on the note')
        return
    sentenceField = fields[sentenceIndex - 1]

    if not note[sentenceField]:
        tooltip(f'{sentenceField} does not have any sentences')
        return

    wordForms = []
    if word:
        wordForms += [word]
        conj_pack = MostLikely.fieldConjugationPack(wordField) #move this outside
        if conj_pack != '—':
            wordForms += [conj for wordForm in Conjugations.conjugate(word, conj_pack) for conj in wordForm["conjs"]]            

    if alt:
        wordForms += [alt]
        conj_pack = MostLikely.fieldConjugationPack(altField) #remove this. determine pack by main field only
        if conj_pack != '—':
            wordForms += [conj for wordForm in Conjugations.conjugate(alt, conj_pack) for conj in wordForm["conjs"]]                        

    for wordForm in wordForms:
        if wordForm in note[sentenceField]:
            note[sentenceField] = note[sentenceField].replace(wordForm, OP + wordForm + ED)
            mw.col.update_note(note)
            editor.loadNoteKeepingFocus()
            tooltip(f'word form {wordForm} highlighted')
            return

    tooltip(f'there is not manual selection and automatic matching did not find any instances of {word}({alt}) in "{sentenceField}"')
    return

def wordHighlight(editor):
    OP = config["highlight"]["tag"]
    ED = closingTag(OP)
    if ED and '>' not in ED:
        tooltip('incorrect highlight tag, check the config')
        return

    selection = editor.web.selectedText()
    if not selection:
        wordHighlightAuto(editor, OP, ED)
        return

    # editor.web.eval(f"document.execCommand('insertHTML', false, {repr(OP + selection + ED)});")

    current_field = editor.currentField
    if current_field is None:
        tooltip('error when determining current_field')
        return

    js_code = f"""
        (function() {{
            try {{
                const activeElement = document.activeElement;
                const shadowRoot = activeElement.shadowRoot;
                const field = shadowRoot.querySelector('[contenteditable="true"]');

                const selection = shadowRoot.getSelection();
                //console.log(selection);
                if (selection.rangeCount > 0) {{
                    const range = selection.getRangeAt(0);
                    const contents = range.extractContents();
                    const tempL = document.createElement('div');
                    tempL.appendChild(contents);
                    tempL.innerHTML = {repr(OP)} + tempL.innerHTML + {repr(ED)};
                    console.log(tempL.innerHTML);
                    range.deleteContents();
                    Array.from(tempL.childNodes).reverse().forEach(node => {{range.insertNode(node.cloneNode(true));}});

                    //selection.removeAllRanges();
                }}

                return JSON.stringify({{ success: "ok" }});
            }} catch (error) {{
                return JSON.stringify({{ error: error.message }});
            }}
        }})();
    """

    def callback(js_result):
        try:
            result = json.loads(js_result)
            if result.get("error"):
                # console.log(result["error"], editor)
                if result["error"] == "Cannot read properties of null (reading 'querySelector')":
                    tooltip("formatted field content should be selected instead of html code")
                return

        except json.JSONDecodeError:
            tooltip("An error occurred while processing the selection!")

    # editor.web.evalWithCallback(js_code, callback)    
    editor.web.eval(js_code)    


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



image_field = ""

editors = ["Photoshop", "GIMP", "Krita"]

def imageEditorQ():
    for editor in editors:
        if editor.lower() in config["image editor"]["path"].lower():
            return editor    
    return "Image Editor"

def images_from_field(field, note):
    imgs = note[field].split("<img")[1:]
    imgs = [img.split(">")[0] for img in imgs]
    imgs = [img.split("src=")[1] for img in imgs]
    imgs = [img.split('"')[1] for img in imgs]

    for img in imgs:
        os.popen(f'{config["image editor"]["path"]} {os.path.join(mw.col.media.dir(), img)}')

def openImages4Editing(editor):
    note = editor.note
    if image_field:
        images_from_field(image_field, note)
    else:
        for field in note.keys():
            images_from_field(field, note)



def setupEditorButtonsFilter(buttons, editor):

    #modify highlight color in the button icons
    icon_folder = os.path.join(addon_path, "icons")
    [updIconHighlightColor(f) for f in os.listdir(icon_folder) if os.path.isfile(os.path.join(icon_folder, f))]


    buttons.insert(0,
        editor.addButton(
            os.path.join(os.path.dirname(__file__), "icons", "ps.svg"),
            'Ps',
            openImages4Editing,
            tip="Open images in " + imageEditorQ()
        )
    )
    buttons.insert(1,
        editor.addButton(
            icon=os.path.join(addon_path, "icons", "contextSearch.svg"),
            cmd='contextSearch',
            func=contextSearch,
            tip="Search for sentences containing the word"
        )
    )
    buttons.insert(2,
        editor.addButton(
            os.path.join(addon_path, "icons", "highlight.svg"),
            'wordHighlight',
            wordHighlight,
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

def injectInlineStyles(web_content, context):

    styles = f"""
    <style>
        [part="word-highlight"],
        div.rich-text-editable::part(word-highlight) {{
            background-color: {config["highlight"]["color"]};
            border-radius: 2px;
            padding: 1px;
        }}
    </style>
    """

    web_content.head += styles


# gui_hooks.editor_did_init_buttons.append(setupEditorButtonsFilter)
addHook("setupEditorButtons", setupEditorButtonsFilter)
gui_hooks.webview_will_set_content.append(injectInlineStyles)