function trigger_loading() {
    var div1 = document.getElementById("loading");
    div1.style.visibility = div1.style.visibility == "hidden" ? "visible" : "hidden";
    var div2 = document.getElementById("live")
    div2.style.visibility = div2.style.visibility == "hidden" ? "visible" : "hidden";
}
