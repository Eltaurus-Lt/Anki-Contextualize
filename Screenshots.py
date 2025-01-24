import os
from aqt import mw

config = mw.addonManager.getConfig(__name__)

overwrite = True

def composeName(source_filename, ts):
    basename, _ = os.path.splitext(os.path.basename(source_filename))
    outputName = f'Contextualize_{basename.replace(" ","")}_{ts}.{config["screenshot extension"]}'.replace(":", ";")
    return outputName

def save(ts, saveas, videoSource):
    fullOutputPath = os.path.join(mw.col.media.dir(), saveas)
    os.popen(f'{config["ffmpeg path"]} {"-y" if overwrite else "-n"} -ss {ts} -i \"{videoSource}\" -vf scale={config["screenshot resolution"]} -frames:v 1 -q:v 7 \"{fullOutputPath}\"')
    return