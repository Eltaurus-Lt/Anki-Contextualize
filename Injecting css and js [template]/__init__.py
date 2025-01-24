import os
from aqt.webview import AnkiWebView, WebContent
from aqt import gui_hooks, mw

addon_folder = os.path.basename(os.path.dirname(__file__))
mw.addonManager.setWebExports(__name__, r".*\.(css|js)$")

def on_webview_will_set_content(web_content: WebContent, context) -> None:
    addon_package = mw.addonManager.addonFromModule(__name__)
    web_content.css.append(os.path.join("/_addons", addon_folder, "style.css"))
    web_content.js.append(os.path.join("/_addons", addon_folder, "script.js"))

gui_hooks.webview_will_set_content.append(on_webview_will_set_content)




