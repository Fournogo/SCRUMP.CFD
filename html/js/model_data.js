'use strict';

let radar_model_animation_index = 0;
let radar_model_image_array = [];
let radar_model_animation_paused = false;
let radar_model_animation_unpaused = true;
let radar_model_minimum_index = 0;

let radar_model_pause_is_clicked = false;
let radar_model_back_is_clicked = false;
let radar_model_next_is_clicked = false;

let path_to_radar_model = '../goes/hrrr_radar/operational/radar-images.json'

let next_radar_model_animation_index = radar_model_animation_index;

async function getRadarModelLinks() {
    let link;
    let element;
    const response = await fetch(path_to_radar_model);
    const json_data = await response.json();
    const image_links = json_data[city.model_state];
    for (let i = 1; i < image_links.length; i++) {
        link = image_links[i];
        element = document.createElement('img');
        element.src = link;
        await element.decode();
        if (i == 0) {
            element.style.opacity = "1";
        } else {
            element.style.opacity = "0";
        }
        document.getElementById('radar-model-images').appendChild(element);
        radar_model_image_array.push(element);
    }
}

function animateRadarModel() { 

    let radar_model_animation_delay;

    let speed_selector = document.getElementById('radar-model-speed-select');
    let speed = speed_selector.value;
    speed = Number(speed);

    if (radar_model_next_is_clicked == true) {
        radar_model_animation_paused = true;
        radar_model_next_is_clicked = false;
        next_radar_model_animation_index = radar_model_animation_index + 1
    }

    if (radar_model_back_is_clicked == true) {
        radar_model_animation_paused = true;
        radar_model_back_is_clicked = false;
        next_radar_model_animation_index = radar_model_animation_index - 1
    }

    if (radar_model_animation_index == radar_model_minimum_index) {
        radar_model_image_array[radar_model_image_array.length - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_animation_index + 1
            radar_model_animation_delay = 1000 / speed
        } else {
            radar_model_animation_delay = 100
        }

    } else if (radar_model_animation_index == radar_model_image_array.length - 1) {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_minimum_index].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_minimum_index
            radar_model_animation_delay = 20000 / speed
        } else {
            radar_model_animation_delay = 100
        }

    } else {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_animation_index + 1
            radar_model_animation_delay = 1000 / speed
        } else {
            radar_model_animation_delay = 100
        }
    }

    if (next_radar_model_animation_index < radar_model_minimum_index) {
        next_radar_model_animation_index = radar_model_image_array.length - 1
    }

    if (next_radar_model_animation_index > radar_model_image_array.length - 1) {
        next_radar_model_animation_index = radar_model_minimum_index
    }

    radar_model_animation_index = next_radar_model_animation_index;
    setTimeout(animateRadarModel, radar_model_animation_delay);
}

function enableRadarModelButtons() {
    document.getElementById('radar-model-pause-button').addEventListener("click", function() {
        if (radar_model_animation_paused == true) {
            radar_model_animation_paused = false;
        } else if (radar_model_animation_paused == false) {
            radar_model_animation_paused = true;
        }
    });
    
    document.getElementById('radar-model-next-button-transparent').style.cursor = "pointer";

    document.getElementById('radar-model-next-button-transparent').addEventListener("click", function() {
        if (radar_model_next_is_clicked == true) {
            radar_model_next_is_clicked = false;
        } else if (radar_model_next_is_clicked == false) {
            radar_model_next_is_clicked = true;
        }
    });

    document.getElementById('radar-model-next-button').addEventListener("click", function() {
        if (radar_model_next_is_clicked == true) {
            radar_model_next_is_clicked = false;
        } else if (radar_model_next_is_clicked == false) {
            radar_model_next_is_clicked = true;
        }
    });

    document.getElementById('radar-model-back-button').addEventListener("click", function() {
        if (radar_model_back_is_clicked == true) {
            radar_model_back_is_clicked = false;
        } else if (radar_model_back_is_clicked == false) {
            radar_model_back_is_clicked = true;
        }
    });
    
}

function clearRadarModelLoading() {
    document.getElementById('radar-model-loading-text').style.opacity = "0";
}

async function animate_radar_model_async() {
    await getRadarModelLinks();
    clearRadarModelLoading();
    enableRadarModelButtons();
    animateRadarModel();
}

function animate_radar_model_main() {
    animate_radar_model_async();
}