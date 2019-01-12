const socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", () => {
    socket.emit("user connected", {});
});
socket.on("update table", (users) => {
    // user['uid'], user['username']
});

$("#send").click(() => {
    socket.emit("user sent message", {
        touid: "ASdfasd",
        data: $("#message_box").val()
    });
});

