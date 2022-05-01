
function toggleTheme() {
  // Obtains an array of all <link> elements.
  var theme = document.getElementsByTagName('link')[0];
//  console.log("got to toggleTheme function")

  // Change the value of href attribute to change the css sheet.
  if (theme.getAttribute('href') == '/static/dist/output.css') {
      theme.setAttribute('href', '/static/fonts/stylesheet.css');
      localStorage.setItem("styleType", "/static/fonts/stylesheet.css");
  } else {
      theme.setAttribute('href', '/static/dist/output.css');
      localStorage.setItem("styleType", "/static/dist/output.css");
  }
}

function setDefault(){
//  console.log("got to setDefault function")
  theme.setAttribute('href', '/static/dist/output.css');// dist
}

function keepCSS(){
  var theme = document.getElementsByTagName('link')[0];
  if (theme.getAttribute('href') == localStorage.getItem("styleType")){ //if style.css is the current styleType, change nothing
  }
  else{
    theme.setAttribute('href', localStorage.getItem("styleType")); //if style.css is not the current styleType, change to style2.css
  }
}

window.onload = function(){
  setDefault();
  keepCSS();
//  console.log("got to onload function")
}
