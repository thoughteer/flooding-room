"use strict";

var socket;
var options;
var room;
var bet_made;

$(document).ready(function() {
    var container = $("#container");

    function update_interface(callback) {
        var water_height = (room.total * 512 / options.points_limit);
        var water = $("#water");
        var bet_overlay = $("#bet_overlay");
        var bet_level = $("#bet_level");
        var bet_overlay_bottom = water_height + 64;
        var bet_overlay_height = Math.min(options.bet_limit * 640.0 / options.points_limit, 640 - water_height + 1);
        bet_overlay.css("bottom", bet_overlay_bottom + "px");
        bet_overlay.css("height", bet_overlay_height + "px");
        var duration = (water_height - water.height()) * 3;
        water.animate({height: water_height}, {duration: duration, queue: false, complete: callback});
        bet_level.animate({bottom: bet_overlay_bottom, height: 0}, {duration: duration, queue: false});
    }

    $("#start_button").click(function() {
        console.log("Connecting...");
        socket = io(document.location.origin);

        socket.on("accept", function (data) {
            options = data;
            $("#start_button").remove();
            $("#start_overlay").html("<img src='static/img/rules1-" + options.player_type + ".png'/>");
            console.log(data);
            socket.emit("check", {"event": "start"});
        });

        socket.on("hold", function (data) {
            console.log("asked to hold: ", data);
            setTimeout(function () {
                console.log("rechecking");
                socket.emit("check", data);
            }, data["period"] * 1000)
        });

        socket.on("decline", function(data) {
            console.error(data["reason"]);
        });

        socket.on("start", function(data) {
            console.info("Game started!");
            room = {total: 0};
            $("#start_overlay").css("display", "none");
            var water = $("<div id='water'></div>");
            var bet_overlay = $("<div id='bet_overlay'></div>");
            var bet_level = $("<div id='bet_level'></div>");
            container.append(bet_level);
            container.append(bet_overlay);
            container.append(water);
            bet_made = false;
            bet_overlay.mousemove(function(event) {
                if (!bet_made) {
                    var height = bet_overlay.height() - event.offsetY;
                    bet_level.css("height", height + "px");
                    //bet_level.stop(true);
                    //bet_level.animate({height: height}, 50);
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
            update_interface();
            socket.emit("check", {"event": "round"})
        });

        socket.on("round", function(data) {
            room.total = data.total;
            update_interface(function() { bet_made = data.is_final; });
            if (data["is_final"]) {
                console.info("Game ended!", data);
            } else {
                socket.emit("check", {"event": "round"})
            }
        });

        socket.emit("ready", {});
    });
});
