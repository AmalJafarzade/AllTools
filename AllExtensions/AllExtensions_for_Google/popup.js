// popup.js

// More Information button click event handler
document.getElementById("infoButton").addEventListener("click", function() {
    // Open a new tab with more information about clickjacking
    chrome.tabs.create({ url: "https://en.wikipedia.org/wiki/Clickjacking" });
  });
  