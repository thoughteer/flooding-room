"use strict";
$(document).ready(function() {
    $("#start_button").click(function() {
        console.log("Connecting...");
        var socket = io("http://localhost:8080");

        socket.on("accept", function (data) {
            $("#start_overlay").remove();
            console.log(data);
        });

        socket.emit("ready", {});
    });
});
