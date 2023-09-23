const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const downloadButton = document.querySelector("#download-btn"); 
let userText = null;
const createChatElement = (content, className) => {
const chatDiv = document.createElement("div");
chatDiv.classList.add("chat", className);
chatDiv.innerHTML = content;
return chatDiv;
    }



    const copyResponse = (copyBtn) => {
    const reponseTextElement = copyBtn.parentElement.querySelector("p");
    navigator.clipboard.writeText(reponseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => copyBtn.textContent = "content_copy", 1000);
    }

const showTypingAnimation = () => {
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="law-and-order.svg">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv);
}



deleteButton.addEventListener("click", () => {
    if(confirm("Are you sure you want to delete all the chats?")) {
        localStorage.removeItem("all-chats");
        loadDataFromLocalstorage();
    }
});
downloadButton.addEventListener("click", async () => {
    /*const fileUrl = "https://example.com/file.txt";
    const fileBlob = new Blob([await fetch(fileUrl).then(response => response.blob())]);
    const anchorElement = document.createElement("p");
    anchorElement.href = window.URL.createObjectURL(fileBlob);
    anchorElement.download = "file.txt";
    anchorElement.click();*/
    document.addEventListener('click', function() {
        var anchorElement = document.createElement('a');
        var fileName = 'file name';
        var fileLink = 'index.html';
        anchorElement.href = fileLink;
        anchorElement.download = fileName;
        anchorElement.target = '_blank';
        document.body.appendChild(anchorElement);
        console.log(anchorElement);
        anchorElement.click();
      })
});

themeButton.addEventListener("click", () => {
  document.body.classList.toggle("light-mode");
  localStorage.setItem("themeColor", document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode");
  themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});





loadDataFromLocalstorage();
sendButton.addEventListener("click", handleOutgoingChat);