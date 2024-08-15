// Arka plan betiği, içerik betiğinden gelen bildirimleri dinler ve gerektiğinde kullanıcıya bildirim gösterir.

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "clickjacking_detected") {
      chrome.notifications.create('clickjackingNotification', {
        type: 'basic',
        iconUrl: 'icon.png',
        title: 'Clickjacking Detected',
        message: 'Clickjacking has been detected on this page.'
      });
    }
  });
  