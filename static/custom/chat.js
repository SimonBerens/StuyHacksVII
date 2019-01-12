const socket = io.connect("http://" + document.domain + ":" + location.port);

socket.on("connect", () => {
    socket.emit("user connected", {});
});
socket.on("update table", (users) => {
    console.log(users);
    // user['uid'], user['username']
    let element = document.getElementByID("people");
    for(let i = 0; i < users.length; i++){
    element.innerHTML += users['username']
  } 
});

$("#send").click(() => {
    socket.emit("user sent message", {
        touid: "sberens",
        data: $("#message_box").val()
    });
});
