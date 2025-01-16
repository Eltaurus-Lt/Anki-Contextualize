import os, re
from aqt.utils import tooltip
Encodings = ['ascii', 'utf-8', 'iso-8859-1', 'latin-1']

def parse(filepath):

    # Open the file in binary mode
    try:
        with open(filepath, 'rb') as file:
            raw_data = file.read()
    except FileNotFound:
        tooltip(f"Subtitle file does not exist ('filepath')")

    # Guess the encoding by trying different encodings
    for tryEncoding in Encodings:
        try:
            # Decode the raw data
            subText = raw_data.decode(tryEncoding)
            encoding = tryEncoding
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        # If all decodings fail, raise an error
        raise ValueError("Unable to decode the file with any common encoding")

    # print(encoding)

    extension = filepath.split('.')[-1]

    if extension == 'ass':
        return assParse(subText)
    elif extension == 'srt':
        return []


def assParse(subText):
    lines = subText.splitlines()
    sentence_db = []

    assPattern = re.compile(r'Dialogue: \d+,(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.+)')

    for line in lines:
        match = assPattern.match(line)
        if match:
            t1 = match.group(1)
            t2 = match.group(2)
            sentence = match.group(9).strip()
            sentence_db.append({'t1': t1, 't2': t2, 'sentence': sentence})

    return sentence_db