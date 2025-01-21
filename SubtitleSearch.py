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