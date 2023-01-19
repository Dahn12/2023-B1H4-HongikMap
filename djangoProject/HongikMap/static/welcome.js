function setup() {
  var e = document.getElementById("watchme");
  e.className = "tracking-in-expand";
}

function listener(e) {
  var l = document.createElement("li");
  document.getElementById("output").appendChild(l);
}
