const socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", () => {
    socket.emit("my event", {
        data: "User Connected"
    });
    $("#send").click(() => {
        socket.emit("my event", {
            data: $("#message_box").val()
        });
    });
});