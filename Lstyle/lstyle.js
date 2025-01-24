function makethumbnail(deck) {
var truncname, cleanname;

cleanname=deck.innerHTML.replace(/^\s*<font style=(""|"color:false;")>\s*/g, ""); //clears "Enhance main window" <font> tag
if (cleanname!=deck.innerHTML) {cleanname=cleanname.replace(/\s*<\/font>\s*$/g, "");} //clears "Enhance main window" </font> tag

cleanname=cleanname.replace(/.*::/g,""); //clears parents names from subdecks

truncname=cleanname.replace(/^([0-9]+\.)+ /g, ""); //removes ordinal numbers

if (truncname!=cleanname) //apply styling to numbered decks only
{deck.innerHTML="<div class=\"deckdiv\"><img src=\"_icons\\"+truncname+".png\" class=\"deckthumbnail\" onerror=\"this.style.display='none'\">"+truncname+"</div>"}
}


window.addEventListener('load', function () {
	document.querySelectorAll('a.deck').forEach((deck) => {makethumbnail(deck)});
	document.querySelectorAll('.isWin h3').forEach((deck) => {makethumbnail(deck)});
})





