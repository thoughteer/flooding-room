"use strict";
$("#start").click(function() {
    var socket = io("http://localhost:8080");
    socket.emit("connect");
});
