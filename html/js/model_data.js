'use strict';

let radar_model_animation_index = 0;
let radar_model_image_array = [];
let radar_model_animation_paused = false;
let radar_model_animation_unpaused = true;
let radar_model_minimum_index = 0;

let radar_model_pause_is_clicked = false;
let radar_model_back_is_clicked = false;
let radar_model_next_is_clicked = false;

let path_to_radar_model = '../goes/hrrr_data/operational/state-model-images.json'

let next_radar_model_animation_index = radar_model_animation_index;

let current_model_selection = 'refd';

let model_speed = 10;
let model_selector = 'refd';

async function getRadarModelLinks() {
    enableRadarModelLoading();
    document.getElementById('model-data-nyancat').style.left = ("0%");
    document.getElementById('model-data-loading-percent').innerText = ("LOADING: 0.0% COMPLETE");
    radar_model_image_array = [];
    let link;
    let element;
    let response = await fetch(path_to_radar_model);
    let json_data = await response.json();
    let image_links = json_data[city.model_state][current_model_selection];

    document.getElementById('radar-model-images').innerHTML = '';

    let percent_increment = (1 / image_links.length);
    let percent_complete = 0;
    let percent_complete_rounded;

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

        percent_complete += percent_increment;
        percent_complete_rounded = ((Math.round(percent_complete * 1000) / 1000) * 100).toFixed(1)
        document.getElementById('model-data-nyancat').style.left = (percent_complete_rounded + "%");
        document.getElementById('model-data-loading-percent').innerText = ("LOADING: " + percent_complete_rounded + "%" + " COMPLETE");
    }
    clearRadarModelLoading();
    radar_model_animation_paused = false;
    radar_model_animation_unpaused = true;
    radar_model_pause_is_clicked = false;
    animateRadarModel();
}

function animateRadarModel() { 

    let radar_model_animation_delay;

    if (model_selector != current_model_selection) {
        current_model_selection = model_selector
        getRadarModelLinks();
        return false
    }

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
            radar_model_animation_delay = 1000 / model_speed
        } else {
            radar_model_animation_delay = 100
        }

    } else if (radar_model_animation_index == radar_model_image_array.length - 1) {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_minimum_index].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_minimum_index
            radar_model_animation_delay = 20000 / model_speed
        } else {
            radar_model_animation_delay = 100
        }

    } else {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_animation_index + 1
            radar_model_animation_delay = 1000 / model_speed
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
    
    document.getElementById('radar-model-images').style.cursor = "pointer";

    document.getElementById('radar-model-images').addEventListener("click", function() {
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

    document.getElementById('radar-model-speed-select').addEventListener('change', function() {
        model_speed = Number(this.value);
    });

    document.getElementById('model-data-selector').addEventListener('change', function() {
        model_selector = this.value;
    });

}

function clearRadarModelLoading() {
    document.getElementById('radar-model-images').style.cursor = "pointer";
    document.getElementById('radar-model-loading-text').style.opacity = "0";
    document.getElementById('radar-model-loading-text').style.zIndex = "-1";
}

function enableRadarModelLoading() {
    document.getElementById('radar-model-images').style.cursor = "auto";
    document.getElementById('radar-model-loading-text').style.opacity = "1";
    document.getElementById('radar-model-loading-text').style.zIndex = "10";
}

async function animate_radar_model_async() {
    await getRadarModelLinks();
    enableRadarModelButtons();
}

function animate_radar_model_main() {
    animate_radar_model_async();
}