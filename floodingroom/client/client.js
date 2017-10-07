"use strict";

var socket;
var options;
var room;
var bet_made;

$(document).ready(function() {
    var container = $("#container");

    function update_interface() {
        var water_height = (room.total * 640 / options.points_limit);
        var water = $("#water");
        var bet_overlay = $("#bet_overlay");
        var bet_level = $("#bet_level");
        water.css("height", water_height + "px");
        var bet_overlay_bottom = water_height + 64;
        var bet_overlay_height = Math.min(options.bet_limit * 640.0 / options.points_limit, 640 - water_height + 1);
        bet_overlay.css("height", bet_overlay_height + "px");
        bet_overlay.css("bottom", bet_overlay_bottom + "px");
        bet_level.css("bottom", bet_overlay_bottom + "px");
    }

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
        });

        socket.on("round", function(data) {
            room.total = data.total;
            bet_made = false;
            update_interface();
        });

        socket.emit("ready", {});
    });
});
