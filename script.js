const sessionId = crypto.randomUUID();

const messagesEl = document.getElementById("messages");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const resetBtn = document.getElementById("resetBtn");

function addMessage(text, cls) {
  const div = document.createElement("div");
  div.className = `msg ${cls}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  const thinking = addMessage("...", "bot");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, session_id: sessionId }),
    });
    const data = await res.json();

    if (!res.ok) {
      thinking.className = "msg error";
      thinking.textContent = data.error || "Something went wrong.";
      return;
    }

    thinking.textContent = data.reply;
  } catch (err) {
    thinking.className = "msg error";
    thinking.textContent = "Network error. Please try again.";
  }
});

resetBtn.addEventListener("click", async () => {
  await fetch("/api/reset", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId }),
  });
  messagesEl.innerHTML = "";
  addMessage("New conversation started.", "bot");
});
