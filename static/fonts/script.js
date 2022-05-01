/*QUICK JS SWITCHER
    Website does not run correctly on newly opened windows or incognito mode most likely due to cache memory or chrome settings. It only works when I click on the button that uses the JS file.
    Quick  JS Switcher refreshes the page so that this is not an issue.

if (chromeContentSettings) {

  var extractHostname = new RegExp('^(?:f|ht)tp(?:s)?\://([^/]+)', 'im'),
    forbiddenOrigin = /(chrome\:\/\/|chrome-extension\:\/\/)/g,
    incognito,
    url,
    setting,
    tabId,
    matchForbiddenOrigin;

  chrome.tabs.onUpdated.addListener(function (tabId, props, tab) {
    // Prevent multiple calls
    if (props.status == "loading" && tab.selected) {
      //console.info("onUpdated");
      getSettings();
    }
  });

  chrome.tabs.onHighlighted.addListener(function () {
    //console.info("onHighlighted");
    getSettings();
  });

  chrome.windows.onFocusChanged.addListener(function () {
    //console.info("onFocusChanged");
    getSettings();
  });

  chrome.windows.getCurrent(function () {
    getSettings();
  });

  chrome.browserAction.onClicked.addListener(changeSettings);


  chrome.commands.onCommand.addListener(function (command) {
    if (command == "toggle-qjs") {

      changeSettings();

    }
  });

  chrome.storage.onChanged.addListener(function (callback) {

    for (var index in callback) {
      if (callback.hasOwnProperty(index)) {
        console.log(callback[index]);
        if (index === 'version') {
          cache[index] = callback[index].newValue;
        } else {
            cache[index] = JSON.parse(callback[index].newValue);
        }
      }
    }

    refresh();

  });


} else {
  chrome.browserAction.onClicked.addListener(openJsPanel.call());
}
*/
/*CSS TOGGLE THEME*/

function toggleTheme() {
  // Obtains an array of all <link> elements.
  var theme = document.getElementsByTagName('link')[0];

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
}
