from aqt.webview import AnkiWebView, WebContent
from aqt import gui_hooks, mw

mw.addonManager.setWebExports(__name__, r".*\.(css|js)$")

def on_webview_will_set_content(web_content: WebContent, context) -> None:
    addon_package = mw.addonManager.addonFromModule(__name__)
    web_content.css.append(f"/_addons/Lstyle/lstyle.css")
    web_content.js.append(f"/_addons/Lstyle/lstyle.js")

gui_hooks.webview_will_set_content.append(on_webview_will_set_content)




