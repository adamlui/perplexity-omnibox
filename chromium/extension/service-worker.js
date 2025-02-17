const perplexityURL = 'https://www.perplexity.ai'

// Launch Perplexity on toolbar icon click
chrome.action.onClicked.addListener(() => chrome.tabs.create({ url: perplexityURL }))

// Query Perplexity on omnibox query submitted
chrome.omnibox.onInputEntered.addListener(query =>
    chrome.tabs.update({ url: `${perplexityURL}/search/new?q=${decodeURIComponent(query)}` }))
