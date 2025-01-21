
import os, json, re

def installedPacks():
    files = os.listdir(os.path.join(os.path.dirname(__file__), 'ConjugationPacks'))
    return [os.path.splitext(file)[0] for file in files if file.endswith('.json')]

def formMatch(word, dictForm):
	regex = dictForm.replace("_", "(.*?)")
	match =  re.fullmatch(regex, word)
	if match:
		wordStems = match.groups()
		return True, wordStems
	else:
		return False, ()

def formReplace(wordStems, conj):
	wordConjugation = ""

	for i in range(len(conj)):
		if conj[i] == '_':
			wordConjugation += wordStems[i]
		else:
			wordConjugation += conj[i]

	return wordConjugation

def conjugate(word, dict, pos = ""):
	wordForms = []

	with open(os.path.join(os.path.dirname(__file__), "ConjugationPacks", f"{dict}.json"), "r", encoding="utf-8") as file:
		dictionary = json.load(file)

	for posCandidate in dictionary: # if posCandidate == pos or not pos (non-blind match)
		for form in posCandidate['forms']:
			match, wordStems = formMatch(word, form['dict'])
			if match:
				wordForms.append({
					"PoS": posCandidate['PoS'],
					"dict": form['dict'],
					"conjs": [formReplace(wordStems, conj['conj']) for conj in form['conjs']]
					})

	return wordForms