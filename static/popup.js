const summarize = document.getElementById("summarize");

const text_div = document.querySelector(".text");

const loader = document.querySelector(".loader");
const summarize_label = document.querySelector(".text-summarized");

let index = 0;
let clicked = false;


summarize.onsubmit = function (e) {
  if(!clicked){
    loader.classList.add("active");
    clicked = true;
  }
  e.preventDefault();
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {
      action: "SUMMARIZE",
    });
  });
  chrome.runtime.onMessage.addListener(function (
    message,
    sender,
    senderResponse
  ) {
    loader.classList.remove("active");
    let summary = message.text.response;
    const summarize_label = document.querySelector(".text-summarized");
    function type() {
      if (index < summary.length) {
        console.log(index)
        summarize_label.innerHTML += summary.charAt(index);
        index++;
        setTimeout(type, 50);
      }
    }    type();
  });
};
