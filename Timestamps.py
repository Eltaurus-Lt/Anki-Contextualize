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

def to_ms(ts):
    us = ts.split(":")
    sec = us[-1].replace(",", ".").split(".")

    us[-1] = sec[0]
    ms = 0
    for u in us:
       ms = 60 * ms
       ms = ms + int(u)
    ms = ms * 1000
    if len(sec) > 1:
        ms = ms + round(int(sec[1]) * 10**(3 - len(sec[1])))

    return ms

def from_ms(ms):
    ms = round(ms)
    sec = ms % 60000
    min = ms // 60000

    hr = min // 60
    min = min % 60

    return f"{hr:02}:{min:02}:{sec//1000:02}.{sec%1000:03}"

def average(t1, t2):
    return from_ms((to_ms(t1) + to_ms(t2)) / 2)
