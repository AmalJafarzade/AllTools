document.addEventListener('DOMContentLoaded', function() {
    var searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            var currentUrl = tabs[0].url;
            var archiveUrl = 'http://web.archive.org/cdx/search/cdx?url=*.' + extractDomain(currentUrl) + '/*&output=txt&fl=original&collapse=urlkey';
            chrome.tabs.create({url: archiveUrl});
        });
    });
});

function extractDomain(url) {
    var domain;
    //find & remove protocol (http, ftp, etc.) and get domain
    if (url.indexOf("://") > -1) {
        domain = url.split('/')[2];
    }
    else {
        domain = url.split('/')[0];
    }

    //find & remove www
    if (domain.indexOf("www.") > -1) {
        domain = domain.split('www.')[1];
    }

    return domain;
}
