## Description

The addon changes the appearance of decks' names in the main window and deck screen, by adding thumbnails and increasing the font size.
It also handles the ordering of decks in the main window.

<p align="middle">
  <img src="https://github.com/Eltaurus-Lt/Lt-Anki-Addons/assets/93875472/b7b2c3c4-af0a-439f-9532-23e4b9c0ba3c" title="Before" style="width:45%">
  <img src="https://github.com/Eltaurus-Lt/Lt-Anki-Addons/assets/93875472/88623baf-5507-4912-a880-bf903a3dff09" title="After" style="width:45%">
</p>

## Installation

Copy the `Lstyle` folder into your `~\addons21\` folder

## Usage

The addon only changes the appearance of the selected decks. In order to mark a deck to be styled by the addon a number followed by a dot and a space should be added to its name:

E.g. `DeckName` → `7. DeckName`
 
<details>
  <summary>details</summary> 
The added number will not be displayed after the styling is applied by the addon. It is only there for marking decks as well as for manually rearranging them on the main screen.
Multiple numbers separated by dots can be used, e.g. "04.8.15. ", which is intended for numbering subdecks but is not necessary.
Numbers can be repeated, so in case manual ordering is not a concern, the same number can be used for all decks, e.g. "0. ".
</details> 

To add thumbnails for decks a folder with the name `_icons` should be created inside `%AnkiUserName%\collection.media\` (default path on Windows is `C:\Users\%WindowsUserName%\AppData\Roaming\Anki2\%AnkiUserName%\collection.media\`). After that, the thumbnails are placed in the `_icons` folder in `.png` format with the filenames corresponding to the decks' names (numbers excluded).
E.g. if the deck's name with the number is `01. DeckName` the thumbnail filename should be `DeckName.png`.
(If a thumbnail file for a numbered deck is not found, the thumbnail does not appear, but the addon still removes the number from the deck's displayed name and changes the font).

## Comments

The addon is tested to work alongside the "Enhance main window" addon.

(c) Lt/22-24
