const socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", () => {
    socket.emit("user connected", {
        sid: "Sdfgs",
        uid: "sdfgsdf"
    });
});

$("#send").click(() => {
    socket.emit("user sent message", {
        touid: "ASdfasd",
        fromuid: "Adsadsfa",
        data: $("#message_box").val()
    });
});