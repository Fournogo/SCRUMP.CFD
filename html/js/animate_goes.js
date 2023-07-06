'use strict';

let goes_animation_index = 0;
let goes_image_array = [];
let goes_animation_paused = false;
let goes_animation_unpaused = true;
let goes_minimum_index = 0;

let goes_pause_is_clicked = false;
let goes_back_is_clicked = false;
let goes_next_is_clicked = false;

let next_goes_animation_index = goes_animation_index;

let number_of_goes_images = 96;
let goes_animation_time = 8;

async function getGoesLinks() {
    let link;
    let final_link;
    let element;
    const response = await fetch(city.goes_json);
    const json_data = await response.json();
    const image_links = json_data.images["1200x1200"];
    for (let i = 0; i < number_of_goes_images; i++) {
        link = image_links[image_links.length + i - number_of_goes_images - 1];
        final_link = city.goes_link + link;
        element = document.createElement('img');
        element.src = final_link;
        await element.decode();
        if (i == 0) {
            element.style.opacity = "1";
        } else {
            element.style.opacity = "0";
        }
        document.getElementById('goes-images').appendChild(element);
        goes_image_array.push(element);
    }
}

function animateGoes() { 

    let goes_animation_delay;

    let speed_selector = document.getElementById('goes-speed-select');
    let speed = speed_selector.value;
    speed = Number(speed);

    let time_selector = document.getElementById('goes-time-select');

    if (goes_animation_time != Number(time_selector.value)) {
        for (let i = 0; i < goes_image_array.length; i++) {
            goes_image_array[i].style.opacity = "0";
        }
        goes_animation_time = Number(time_selector.value);
        goes_minimum_index = (number_of_goes_images - (goes_animation_time * 12));
        goes_animation_index = goes_minimum_index
    }

    if (goes_next_is_clicked == true) {
        goes_animation_paused = true;
        goes_next_is_clicked = false;
        next_goes_animation_index = goes_animation_index + 1
    }

    if (goes_back_is_clicked == true) {
        goes_animation_paused = true;
        goes_back_is_clicked = false;
        next_goes_animation_index = goes_animation_index - 1
    }

    if (goes_animation_index == goes_minimum_index) {
        goes_image_array[goes_image_array.length - 1].style.opacity = "0";
        goes_image_array[goes_animation_index].style.opacity = "1";
        goes_image_array[goes_animation_index + 1].style.opacity = "0";
        if (goes_animation_paused == false) {
            next_goes_animation_index = goes_animation_index + 1
            goes_animation_delay = 1000 / speed
        } else {
            goes_animation_delay = 0
        }

    } else if (goes_animation_index == goes_image_array.length - 1) {
        goes_image_array[goes_animation_index - 1].style.opacity = "0";
        goes_image_array[goes_animation_index].style.opacity = "1";
        goes_image_array[goes_minimum_index].style.opacity = "0";
        if (goes_animation_paused == false) {
            next_goes_animation_index = goes_minimum_index
            goes_animation_delay = 20000 / speed
        } else {
            goes_animation_delay = 0
        }

    } else {
        goes_image_array[goes_animation_index - 1].style.opacity = "0";
        goes_image_array[goes_animation_index].style.opacity = "1";
        goes_image_array[goes_animation_index + 1].style.opacity = "0";
        if (goes_animation_paused == false) {
            next_goes_animation_index = goes_animation_index + 1
            goes_animation_delay = 1000 / speed
        } else {
            goes_animation_delay = 0
        }
    }

    if (next_goes_animation_index < goes_minimum_index) {
        next_goes_animation_index = goes_image_array.length - 1
    }

    if (next_goes_animation_index > goes_image_array.length - 1) {
        next_goes_animation_index = goes_minimum_index
    }

    goes_animation_index = next_goes_animation_index;
    setTimeout(animateGoes, goes_animation_delay);
}

function enableGoesButtons() {
    document.getElementById('goes-pause-button').addEventListener("click", function() {
        if (goes_animation_paused == true) {
            goes_animation_paused = false;
        } else if (goes_animation_paused == false) {
            goes_animation_paused = true;
        }
    });
    
    document.getElementById('goes-next-button-transparent').style.cursor = "pointer";

    document.getElementById('goes-next-button-transparent').addEventListener("click", function() {
        if (goes_next_is_clicked == true) {
            goes_next_is_clicked = false;
        } else if (goes_next_is_clicked == false) {
            goes_next_is_clicked = true;
        }
    });

    document.getElementById('goes-next-button').addEventListener("click", function() {
        if (goes_next_is_clicked == true) {
            goes_next_is_clicked = false;
        } else if (goes_next_is_clicked == false) {
            goes_next_is_clicked = true;
        }
    });

    document.getElementById('goes-back-button').addEventListener("click", function() {
        if (goes_back_is_clicked == true) {
            goes_back_is_clicked = false;
        } else if (goes_back_is_clicked == false) {
            goes_back_is_clicked = true;
        }
    });
    
}

function clearGoesLoading() {
    document.getElementById('goes-loading-text').style.opacity = "0";
}

async function animate_goes_async() {
    await getGoesLinks();
    clearGoesLoading();
    enableGoesButtons();
    animateGoes();
}

function animate_goes_main() {
    animate_goes_async();
}