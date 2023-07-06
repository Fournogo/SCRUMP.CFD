'use strict';

function radar() {
    document.getElementById('radar-loop').src = city.radar_loop
    document.getElementById('radar-latest').src = city.radar_latest
    };

let radar_paused = false;

let radar_images = document.getElementById('radar-holder').children;

document.getElementById('radar-button').addEventListener("click", function() {
    if (radar_paused == false) {
        radar_paused = true;
        radar_images[0].style.opacity = "0";
        radar_images[1].style.opacity = "1";
    } else if (radar_paused == true) {
        radar_paused = false;
        radar_images[0].style.opacity = "1";
        radar_images[1].style.opacity = "0";
    }
});
