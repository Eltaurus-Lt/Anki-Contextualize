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

from . import Conjugations

def searchExact(word, sentence_db):
    for entry in sentence_db:
        if word in entry['sentence']:
            return {'t1': entry['t1'], 't2': entry['t2'], 'sentence': entry['sentence'], 'word_form': word}

    return {}

def searchConjugated(word, sentence_db, conj_pack, pos = ""):
    # dict form
    word = word.replace("&nbsp;", " ").strip()
    if not bool(word):
        return {}

    searchResult = searchExact(word, sentence_db)
    if searchResult:
        return searchResult

    # conj forms

    if conj_pack == '—' or not bool(conj_pack):
        return {}

    # blind match
    wordForms = Conjugations.conjugate(word, conj_pack) # add pos here if not empty for non-blind
    for wordForm in wordForms:
        for conj in wordForm['conjs']:
            searchResult = searchExact(conj, sentence_db)
            if searchResult:
                return searchResult

    return {}