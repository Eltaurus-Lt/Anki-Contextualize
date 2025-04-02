# This script is part of the Contextualize Add-on for Anki.
# Source: https://github.com/Eltaurus-Lt/Anki-Contextualize
# 
# Copyright © 2024 Eltaurus
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