"use strict";

var socket;
var options;
var room;

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

        socket.on("start", function(data) {
            console.info("Game started!");
            room = {total: 0};
            $("#start_overlay").css("display", "none")
            var bet_overlay = $("<div id='bet_overlay'></div>");
            bet_overlay.css("height", options.bet_limit + "px");
            bet_overlay.css("bottom", (room.total + 64) + "px");
            var bet_level = $("<div id='bet_level'></div>");
            bet_level.css("bottom", (room.total + 64) + "px");
            $("#container").append(bet_level);
            $("#container").append(bet_overlay);
            $(bet_overlay).mousemove(function(event) {
                var height = $(bet_overlay).height() - event.offsetY;
                $(bet_level).css("height", height + "px");
            });
        });

        socket.emit("ready", {});
    });
});
