function getTranscript() {
  console.log(message);
  console.log("Listened");
  const url = window.location.href;
  fetch(`http://localhost:2000/api/summarize?youtube_url=${url}`).then(
    (response) => response.json().then(data =>   chrome.runtime.sendMessage({ text: data }))
  );
}

chrome.runtime.onMessage.addListener(function (message) {
  console.log(message)
  getTranscript()
});
