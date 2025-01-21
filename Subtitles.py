import os, re
# from aqt.utils import tooltip
Encoding_candidates = ['ascii', 'utf-8', 'iso-8859-1', 'latin-1']

def parse(filepath):
    if not bool(filepath):
        return []

    # Open the file in binary mode
    try:
        with open(filepath, 'rb') as file:
            raw_data = file.read()
    except FileNotFound:
        tooltip(f"Subtitle file does not exist ('filepath')")

    # Guess the encoding by trying different encodings
    for candidate in Encoding_candidates:
        try:
            # Decode the raw data
            subText = raw_data.decode(candidate)
            encoding = candidate
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        # If all decodings fail, raise an error
        raise ValueError("Unable to decode the file with any common encoding")

    # print(encoding)
    # print(subText)

    extension = filepath.split('.')[-1]

    subText = subText.replace("\r\n","\n").replace("\r","\n")

    if extension == 'ass':
        return assParse(subText)
    if extension == 'srt':
        return srtParse(subText)
    if extension == 'sub':
        return subParse(subText)


def assParse(subText):
    lines = subText.splitlines()
    sentence_db = []

    pattern = re.compile(r'Dialogue: \d+,(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.+)')

    for line in lines:
        match = pattern.match(line)
        if match:
            t1 = match.group(1)
            t2 = match.group(2)
            sentence = match.group(9).strip()
            sentence_db.append({'t1': t1, 't2': t2, 'sentence': sentence})

    return sentence_db

def srtParse(subText):
    sentence_db = []

    pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    matches = pattern.findall(subText)

    for match in matches:
        t1, t2, sentence = match
        t1 = t1.replace(",", ".")
        t2 = t2.replace(",", ".")
        sentence_db.append({'t1': t1, 't2': t2, 'sentence': sentence})

    return sentence_db

def subParse(subText):
    return []