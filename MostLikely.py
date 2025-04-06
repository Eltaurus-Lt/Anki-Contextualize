from aqt import mw
from fnmatch import fnmatch
from . import Conjugations

config = mw.addonManager.getConfig(__name__)

def imageEditor():
    for editor in ["Photoshop", "GIMP", "Krita"]:
        if editor.lower() in config["image editor"]["path"].lower():
            return editor    
    return "Image Editor"

def fieldIndex(fields, category):
    fields = [field.lower() for field in fields]
    candidates = [candidate.lower() for candidate in config["fields"][category]]
    for candidate in candidates:
        if candidate in fields:
            return fields.index(candidate)
        for field in fields:
            if fnmatch(field, candidate):
                return fields.index(field)
            
    return 0

def fieldConjugationPack(field):
    rules = config["fields"]["conjugation rules"]
    for lang in rules.keys():
        if lang.lower() in field.lower() and rules[lang] in Conjugations.installedPacks():
            return rules[lang]

    return '—'