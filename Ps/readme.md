## Description

The Add-on appends a new button to the Anki editor toolbar that allows opening images from a card in Photoshop with a single click.

![image](https://github.com/Eltaurus-Lt/Lt-Anki-Addons/assets/93875472/571ea553-069c-4aa1-9ebc-aec1555a671e)


## Installation and setup

- Copy the `Ps` folder into your `~\addons21\` folder
- (optional) Open `__init__.py` in any text editor and enter the name of a field on your note type dedicated to images inside the quotation marks in the line `image_field = ""`. <br><sub>If the string is left empty, the addon will always open all images from all fields of a card. If there is only one field that contains images, specifying its name here is not necessary and won't have an effect.</sub>
- Make sure Photoshop is added to the PATH system variable. <br><sub>Alternatively, replace the word `photoshop` in the line `os.popen(f'photoshop -o {os.path.join(mw.col.media.dir(), img)}')` with a full path to your Photoshop exe file. Other image editors can also be specified here instead.</sub>

## Usage

Simply press the button ![image](https://github.com/Eltaurus-Lt/Lt-Anki-Addons/assets/93875472/540304b6-63d3-4ff9-884a-5784b918a202) on an Anki editor toolbar to open images contained within a card in Photoshop. After the editing of an image is done, save it without changing the name of the file and close it. No further actions are needed. The changes will not be visible in Anki right away, as it displays the cached versions of images, but the updates will take effect eventually. You can restart Anki to force it to clear the cache and display the images with the latest changes.

(c) Lt/24
