const socket = io();
let currentUser = null;

// On page load, get current user from server
window.addEventListener('load', () => {
    // For now, we get username from sessionStorage (set after login)
    // In production, you'd fetch this from server
    currentUser = sessionStorage.getItem('username');
    
    if (!currentUser) {
        // If no user in session, redirect to login
        window.location.href = "/login";
    } else {
        document.getElementById("current-user").textContent = currentUser;
    }
});

function sendMessage() {
    const msg = document.getElementById("msg").value.trim();
    
    if (!msg) return;
    
    socket.emit("message", {username: currentUser, message: msg});
    document.getElementById("msg").value = "";
}

function logout() {
    sessionStorage.removeItem('username');
    window.location.href = "/login";
}

socket.on("message", (data) => {
    const messagesDiv = document.getElementById("messages");
    const messageItem = document.createElement("div");
    messageItem.className = "message-item";
    messageItem.innerHTML = `<strong>${data.username}</strong><p>${data.message}</p>`;
    messagesDiv.appendChild(messageItem);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

// Allow Enter key to send message
document.getElementById("msg").addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});