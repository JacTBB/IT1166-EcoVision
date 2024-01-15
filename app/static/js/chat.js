var socketio = io();

const messages = document.getElementById("messages");

const createMessage = (name, msg) => {
    const content = `
  <div class="text">
      <span>
          <strong>${name}</strong>: ${msg}
      </span>
      <span class="muted">
          ${new Date().toLocaleString()}
      </span>
  </div>
  `;
    messages.innerHTML += content;
};

socketio.on("message", (data) => {
    console.log("receive", data)
    createMessage(data.name, data.message);
});

const userDisconnected = () => {
    socketio.emit("userDisconnected", {});
};

const sendMessage = () => {
    const message = document.getElementById("message");
    console.log("send", message.value)
    if (message.value == "") return;
    socketio.emit("message", { data: message.value });
    message.value = "";
};

$(window).on("load", function () {
    socketio.emit("requestRoom", {});
});

$(window).on("beforeunload", function () {
    userDisconnected();
});

$(document).ready(function () {
    var popup = $(".chat-popup");
    var chatBtn = $(".chat-btn");

    chatBtn.on('click', () => {
        popup.toggleClass('show');
    })
}); 