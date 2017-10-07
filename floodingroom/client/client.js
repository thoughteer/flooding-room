"use strict";

var socket;
var options;
var room;

$(document).ready(function() {
    var container = $("#container");

    $("#start_button").click(function() {
        console.log("Connecting...");
        socket = io("http://localhost:8080");

        socket.on("accept", function (data) {
            options = data;
            $("#start_button").remove();
            $("#start_overlay").html("<img src='static/img/rules1-" + options.player_type + ".png'/>");
            console.log(data);
            socket.emit("check", {});
        });

        socket.on("hold", function (data) {
            console.log("asked to hold: ", data)
            setTimeout(function () {
                console.log("rechecking")
                socket.emit("check", {});
            }, data["period"] * 1000)
        });

        socket.on("decline", function(data) {
            console.error(data["reason"]);
        });

        socket.on("start", function(data) {
            console.info("Game started!");
            room = {total: 0};
            $("#start_overlay").css("display", "none")
            var bet_overlay = $("<div id='bet_overlay'></div>");
            bet_overlay.css("height", (options.bet_limit * 640.0 / options.points_limit) + "px");
            bet_overlay.css("bottom", (room.total + 64) + "px");
            var bet_level = $("<div id='bet_level'></div>");
            bet_level.css("bottom", (room.total + 64) + "px");
            container.append(bet_level);
            container.append(bet_overlay);
            var bet_made = false;
            bet_overlay.mousemove(function(event) {
                if (!bet_made) {
                    var height = bet_overlay.height() - event.offsetY;
                    bet_level.css("height", height + "px");
                }
            });
            bet_overlay.mouseup(function(event) {
                var height = bet_overlay.height() - event.offsetY;
                bet_level.css("height", height + "px");
                var bet = options.bet_limit * height / bet_overlay.height();
                console.info("Making bet:", bet);
                socket.emit("bet", {bet: bet});
                bet_made = true;
            });
        });

        socket.emit("ready", {});
    });
});
