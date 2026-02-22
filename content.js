// Listens for a request from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "get_page_text") {
        // Grabs all the visible text on the active website
        sendResponse({ text: document.body.innerText });
    }
    return true; 
});