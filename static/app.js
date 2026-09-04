const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const messages = document.getElementById("messages");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");
let history = [];

function addMessage(role, text) {
  const row = document.createElement("div");
  row.className = `message ${role}`;
  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "assistant" ? "a" : "you";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  row.append(avatar, bubble);
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}

function addTyping() {
  const row = document.createElement("div");
  row.className = "message assistant typing-row";
  row.innerHTML = '<div class="message-avatar">a</div><div class="bubble typing"><i></i><i></i><i></i></div>';
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
  return row;
}

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 140)}px`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text || sendButton.disabled) return;
  addMessage("user", text);
  history.push({ role: "user", content: text });
  input.value = "";
  input.style.height = "auto";
  sendButton.disabled = true;
  const typing = addTyping();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text, history })
    });
    const data = await response.json();
    typing.remove();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    addMessage("assistant", data.answer);
    history.push({ role: "model", content: data.answer });
  } catch (error) {
    typing.remove();
    addMessage("assistant", error.message || "I couldn’t respond right now. Please try again.");
    history.pop();
  } finally {
    sendButton.disabled = false;
    input.focus();
  }
});

clearButton.addEventListener("click", () => {
  history = [];
  messages.innerHTML = "";
  addMessage("assistant", "Fresh start. What would you like to explore?");
  input.focus();
});

input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});