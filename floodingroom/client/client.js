"use strict";

var socket;
var options;

$(document).ready(function() {
    $("#start_button").click(function() {
        console.log("Connecting...");
        socket = io("http://localhost:8080");

        socket.on("accept", function (data) {
            options = data;
            $("#start_button").remove();
            $("#start_overlay").html("<img src='static/img/rules1-" + options.player_type + ".png'/>");
            console.log(data);
        });

        socket.on("decline", function(data) {
            console.error(data["reason"]);
        });

        socket.emit("ready", {});
    });
});
