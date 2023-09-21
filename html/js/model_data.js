'use strict';

let radar_model_animation_index = 0;
let radar_model_image_array = [];
let radar_model_hours_array = [];
let radar_model_animation_paused = false;
let radar_model_animation_unpaused = true;
let radar_model_minimum_index = 0;

let radar_model_pause_is_clicked = false;
let radar_model_back_is_clicked = false;
let radar_model_next_is_clicked = false;

let path_to_radar_model = '../goes/json/'
let file_name = 'model_data.json'

let next_radar_model_animation_index = radar_model_animation_index;

let current_forecast_selection = 'refd';
let current_product_selection = 'subh';
let current_model_selection = 'hrrr';

let model_speed = 10;
let forecast_selector = 'refd';
let product_selector = 'subh';
let model_selector = 'hrrr';

let added_options = [];

let radar_model_animation_delay;

async function getRadarModelLinks() {
    enableRadarModelLoading();
    document.getElementById('model-data-nyancat').style.left = ("0%");
    document.getElementById('model-data-loading-percent').innerText = ("LOADING: 0.0% COMPLETE");
    radar_model_image_array = [];
    let link;
    let element;
    let response = await fetch(path_to_radar_model + file_name);
    let json_data = await response.json();

    let names_response = await fetch(path_to_radar_model + 'names.json')
    let names = await names_response.json();

    document.getElementById('product-selector').innerHTML = ''
    document.getElementById('forecast-selector').innerHTML = ''

    added_options = [];

    if (current_model_selection != model_selector) {
        current_model_selection = model_selector;
        current_product_selection = Object.keys(json_data[current_model_selection])[0];
        current_forecast_selection = Object.keys(json_data[current_model_selection][current_product_selection])[0];
        product_selector = current_product_selection;
        forecast_selector = current_forecast_selection;
    } else {
        current_model_selection = model_selector;
        current_forecast_selection = forecast_selector;
        current_product_selection = product_selector;
    }

    for (let model of Object.keys(json_data)) {
        if (model = current_model_selection) {
            for (let product of Object.keys(json_data[model])) {
                for (let forecast of Object.keys(json_data[model][product])) {
                    let forecast_option = document.createElement("option");
                    forecast_option.text = names[forecast];
                    forecast_option.value = forecast;

                    let product_option = document.createElement("option");
                    product_option.text = names[product];
                    product_option.value = product;

                    if (product == current_product_selection) {
                        product_option.selected = true;
                    }

                    if (forecast == current_forecast_selection) {
                        forecast_option.selected = true;
                    }

                    if (!added_options.includes(product)) {
                        added_options.push(product);
                        document.getElementById('product-selector').appendChild(product_option);
                    }

                    if (!added_options.includes(forecast)) {
                        added_options.push(forecast);
                        document.getElementById('forecast-selector').appendChild(forecast_option);
                    }
                }
            }
        }
    }
    
    console.log(current_model_selection);
    console.log(current_product_selection);
    let image_links = json_data[current_model_selection][current_product_selection][current_forecast_selection][city.state];
    document.getElementById('radar-model-images').innerHTML = '';

    let percent_increment = (1 / image_links.length);
    let percent_complete = 0;
    let percent_complete_rounded;

    radar_model_hours_array = image_links.map(extractNumbers);

    radar_model_hours_array = radar_model_hours_array.map((value, index, array) => {
        if (index < array.length - 1) {
          return array[index + 1] - value;
        }
        return value - array[index - 1]; // Handle the last element (no next element to subtract)
    });

    console.log(radar_model_hours_array)

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

        if (forecast_selector != current_forecast_selection || product_selector != current_product_selection || model_selector != current_model_selection) {
            //current_model_selection = model_selector
            getRadarModelLinks();
            return false;
        }
    }

    clearRadarModelLoading();
    radar_model_animation_paused = false;
    radar_model_animation_unpaused = true;
    radar_model_pause_is_clicked = false;

    radar_model_animation_index = 0;
    animateRadarModel();
}

function animateModel() {
    setTimeout(animateRadarModel, radar_model_animation_delay);
}

// Function to extract the numbers from the filenames with a regex
function extractNumbers(filename) {
    const pattern = /_(\d+)\./;
    const match = filename.match(pattern);
    if (match && match[1]) {
      return Number(match[1]); // The extracted number
    }
    return null; // Return null if no match is found
}

function animateRadarModel() { 

    if (forecast_selector != current_forecast_selection || product_selector != current_product_selection || model_selector != current_model_selection) {
        //current_model_selection = model_selector
        getRadarModelLinks();
        return false;
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
            radar_model_animation_delay = (1000 / model_speed) * radar_model_hours_array[radar_model_animation_index];
        } else {
            radar_model_animation_delay = 100;
        }

    } else if (radar_model_animation_index == radar_model_image_array.length - 1) {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_minimum_index].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_minimum_index
            radar_model_animation_delay = 20000 / model_speed;
        } else {
            radar_model_animation_delay = 100;
        }

    } else {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_animation_index + 1
            radar_model_animation_delay = (1000 / model_speed) * radar_model_hours_array[radar_model_animation_index];
        } else {
            radar_model_animation_delay = 100;
        }
    }

    if (next_radar_model_animation_index < radar_model_minimum_index) {
        next_radar_model_animation_index = radar_model_image_array.length - 1;
    }

    if (next_radar_model_animation_index > radar_model_image_array.length - 1) {
        next_radar_model_animation_index = radar_model_minimum_index;
    }

    radar_model_animation_index = next_radar_model_animation_index;
    console.log(radar_model_animation_delay)
    requestAnimationFrame(animateModel);
    //setTimeout(animateRadarModel, radar_model_animation_delay);
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
}

function enableForecastBrowser() {
    document.getElementById('forecast-selector').addEventListener('change', function() {
        forecast_selector = this.value;
    });

    document.getElementById('model-selector').addEventListener('change', function() {
        model_selector = this.value;
    });

    document.getElementById('product-selector').addEventListener('change', function() {
        product_selector = this.value;
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
    enableForecastBrowser();
    await getRadarModelLinks();
    enableRadarModelButtons();
}

function animate_radar_model_main() {
    animate_radar_model_async();
}