import os
from aqt import mw
# configs
overwrite = True
default_ext = "jpg"

def composeName(source_filename, ts):
    basename, _ = os.path.splitext(os.path.basename(source_filename))
    outputName = f'Contextualize_{basename}_{ts}.{default_ext}'.replace(":", ";")
    return outputName

def save(ts, saveas, videoSource):
    fullOutputPath = os.path.join(mw.col.media.dir(), saveas)
    os.popen(f'ffmpeg {"-y" if overwrite else "-n"} -ss {ts} -i \"{videoSource}\" -vf scale=720:-1 -frames:v 1 -q:v 7 \"{fullOutputPath}\"')
    return