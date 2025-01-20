
import os, json, re

def formMatch(word, dictForm):
	regex = dictForm.replace("_", "(.*?)")
	match =  re.fullmatch(regex, word)
	if match:
		wordStems = match.groups()
		return True, wordStems
	else:
		return False, ()

def formReplace(wordStems, conj):
	wordForm = ""

	for i in range(len(conj)):
		if conj[i] == '_':
			wordForm += wordStems[i]
		else:
			wordForm += conj[i]

	return wordForm

def conjugate(word, dict, pos = ""):
	wordConjugations = []

	with open(os.path.join("LanguagePacks", f"{dict}.json"), "r", encoding="utf-8") as file:
		dictionary = json.load(file)

	for posCandidate in dictionary: # if posCandidate == pos or not pos (non-blind match)
		for form in posCandidate['forms']:
			match, wordStems = formMatch(word, form['dict'])
			if match:
				wordConjugations.append({
					"PoS": posCandidate['PoS'],
					"dict": form['dict'],
					"conjs": [formReplace(wordStems, conj['conj']) for conj in form['conjs']]
					})

	return wordConjugations