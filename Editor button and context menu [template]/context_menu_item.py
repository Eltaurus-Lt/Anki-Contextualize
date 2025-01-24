import os
from aqt.qt import *
from aqt import gui_hooks

from aqt.utils import tooltip

addon_path = os.path.dirname(__file__)

def menu_action(browser):
    tooltip('menu item is selected')

def setup_context_menu(browser):
    menu = browser.form.menu_Cards
    action = menu.addAction("M&enu item")
    qconnect(action.triggered, lambda: menu_action(browser))


gui_hooks.browser_menus_did_init.append(setup_context_menu)