const socket = io();
 
function showMessage(text, type) {
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = text;
    messageDiv.className = "message " + type;
}
 
function register() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    
    if (!username || !password) {
        showMessage("Enter username and password", "error");
        return;
    }
    
    socket.emit("register", {username, password});
}
 
function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    
    if (!username || !password) {
        showMessage("Enter username and password", "error");
        return;
    }
    
    socket.emit("login", {username, password});
}
 
socket.on("register_response", (data) => {
    if (data.error) {
        showMessage(data.error, "error");
    } else {
        showMessage("Account created! Now login.", "success");
        document.getElementById("username").value = "";
        document.getElementById("password").value = "";
    }
});
 
socket.on("login_response", (data) => {
    if (data.error) {
        showMessage(data.error, "error");
    } else {
        // Store username in sessionStorage so chat page can access it
        sessionStorage.setItem('username', data.username);
        // Redirect to chat page after successful login
        window.location.href = "/";
    }
});