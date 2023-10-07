'use strict';

let radar_model_animation_index = 0;
let radar_model_image_array = [];
let radar_model_hours_array = [];
let radar_model_animation_paused = false;
let radar_model_animation_unpaused = true;
let model_data_min_index = 0;
let model_data_max_index;

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
let slider_value = 0;

let added_options = [];

let radar_model_animation_delay;

let sliding = false;
let regions;
let model_data;
let common_names;

async function getRegions() {
    let response = await fetch('../goes/json/regions.json');
    regions = await response.json();
}   

async function getModelData() {
    let response = await fetch(path_to_radar_model + file_name);
    model_data = await response.json();
}

async function getNames() {
    let names_response = await fetch(path_to_radar_model + 'names.json')
    common_names = await names_response.json();
}

function resetRegions(model) {
    document.getElementById('region-selector').innerHTML = ''
    let region_list = regions[model];
    current_region_selection = Object.keys(region_list)[0];

    for (let region of Object.keys(region_list)) {
        let region_option = document.createElement("option");
        region_option.text = region_list[region];
        region_option.value = region;

        if (region == current_region_selection) {
            region_option.selected == true;
        }

        document.getElementById('region-selector').appendChild(region_option);
    }
}

async function getRadarModelLinks() {
    enableRadarModelLoading();
    document.getElementById('model-data-nyancat').style.left = ("0%");
    document.getElementById('model-data-loading-percent').innerText = ("LOADING: 0.0% COMPLETE");
    radar_model_image_array = [];
    let link;
    let element;

    document.getElementById('product-selector').innerHTML = ''
    document.getElementById('forecast-selector').innerHTML = ''

    added_options = [];

    if (current_model_selection != model_selector) {
        current_model_selection = model_selector;
        resetRegions(current_model_selection);
        current_product_selection = Object.keys(model_data[current_model_selection])[0];
        current_forecast_selection = Object.keys(model_data[current_model_selection][current_product_selection])[0];
        product_selector = current_product_selection;
        forecast_selector = current_forecast_selection;
    } else {
        current_model_selection = model_selector;
        current_region_selection = region_selector;
        current_forecast_selection = forecast_selector;
        current_product_selection = product_selector;
    }

    for (let model of Object.keys(model_data)) {
        if (model = current_model_selection) {
            for (let product of Object.keys(model_data[model])) {
                for (let forecast of Object.keys(model_data[model][product])) {
                    let forecast_option = document.createElement("option");
                    forecast_option.text = common_names[forecast];
                    forecast_option.value = forecast;

                    let product_option = document.createElement("option");
                    product_option.text = common_names[product];
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
    console.log(current_model_selection)
    console.log(current_product_selection)
    console.log(current_forecast_selection)
    console.log(current_region_selection)
    let image_links = model_data[current_model_selection][current_product_selection][current_forecast_selection][current_region_selection];
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

        if (forecast_selector != current_forecast_selection || 
            product_selector != current_product_selection || 
            model_selector != current_model_selection ||
            region_selector != current_region_selection
            ) {
            //current_model_selection = model_selector
            getRadarModelLinks();
            return false;
        }

        model_data_max_index = radar_model_image_array.length - 1 

        document.getElementById('forecast-slider').min = model_data_min_index
        document.getElementById('forecast-slider').max = model_data_max_index

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

    if (sliding == true) {
        return false;
    }

    if (forecast_selector != current_forecast_selection || 
        product_selector != current_product_selection || 
        model_selector != current_model_selection ||
        region_selector != current_region_selection) {
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

    if (radar_model_animation_index == model_data_min_index) {
        radar_model_image_array[model_data_max_index].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = radar_model_animation_index + 1
            radar_model_animation_delay = (1000 / model_speed) * radar_model_hours_array[radar_model_animation_index];
        } else {
            radar_model_animation_delay = 100;
        }

    } else if (radar_model_animation_index == model_data_max_index) {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index].style.opacity = "1";
        radar_model_image_array[model_data_min_index].style.opacity = "0";
        if (radar_model_animation_paused == false) {
            next_radar_model_animation_index = model_data_min_index
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

    if (next_radar_model_animation_index < model_data_min_index) {
        next_radar_model_animation_index = model_data_max_index;
    }

    if (next_radar_model_animation_index > model_data_max_index) {
        next_radar_model_animation_index = model_data_min_index;
    }

    radar_model_animation_index = next_radar_model_animation_index;
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
        if (sliding == true) {
            sliding = false;
            next_radar_model_animation_index = radar_model_animation_index + 1;
            animateRadarModel();
        }
    });
    
    document.getElementById('radar-model-images').style.cursor = "pointer";

    document.getElementById('radar-model-images').addEventListener("click", function() {
        if (radar_model_next_is_clicked == true) {
            radar_model_next_is_clicked = false;
        } else if (radar_model_next_is_clicked == false) {
            radar_model_next_is_clicked = true;
        }
        if (sliding == true) {
            sliding = false;
            next_radar_model_animation_index = radar_model_animation_index + 1;
            animateRadarModel();
        }
    });

    document.getElementById('radar-model-next-button').addEventListener("click", function() {
        if (radar_model_next_is_clicked == true) {
            radar_model_next_is_clicked = false;
        } else if (radar_model_next_is_clicked == false) {
            radar_model_next_is_clicked = true;
        }
        if (sliding == true) {
            sliding = false;
            next_radar_model_animation_index = radar_model_animation_index + 1;
            animateRadarModel();
        }
    });

    document.getElementById('radar-model-back-button').addEventListener("click", function() {
        if (radar_model_back_is_clicked == true) {
            radar_model_back_is_clicked = false;
        } else if (radar_model_back_is_clicked == false) {
            radar_model_back_is_clicked = true;
        }
        if (sliding == true) {
            sliding = false;
            next_radar_model_animation_index = radar_model_animation_index + 1;
            animateRadarModel();
        }
    });

    document.getElementById('radar-model-speed-select').addEventListener('change', function() {
        model_speed = Number(this.value);
    });
}

function sliderHandler(value) {
    if (sliding == false) {
        if (radar_model_animation_index != model_data_min_index) {
            radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
        } else {
            radar_model_image_array[model_data_max_index].style.opacity = "0";
        }
        sliding = true;
    }

    slider_value = Number(value);

    radar_model_image_array[radar_model_animation_index].style.opacity = "0";
    radar_model_animation_index = slider_value;

    radar_model_animation_paused = true;
    console.log(radar_model_animation_index)
    console.log(slider_value)
    if (slider_value != model_data_max_index && slider_value != model_data_min_index) {
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
    } else if (slider_value == model_data_max_index) {
        radar_model_image_array[radar_model_animation_index - 1].style.opacity = "0";
    } else if (slider_value == model_data_min_index) {
        radar_model_image_array[radar_model_animation_index + 1].style.opacity = "0";
    }
    //next_radar_model_animation_index = radar_model_animation_index + 1;
    radar_model_image_array[radar_model_animation_index].style.opacity = "1";
}

function enableForecastBrowser() {
    document.getElementById('forecast-selector').addEventListener('change', function() {
        forecast_selector = this.value;
        if (sliding == true) {
            sliding = false;
            getRadarModelLinks();
            return false;
        }
    });

    document.getElementById('model-selector').addEventListener('change', function() {
        model_selector = this.value;
        if (sliding == true) {
            sliding = false;
            getRadarModelLinks();
            return false;
        }
    });

    document.getElementById('product-selector').addEventListener('change', function() {
        product_selector = this.value;
        if (sliding == true) {
            sliding = false;
            getRadarModelLinks();
            return false;
        }
    });

    document.getElementById('region-selector').addEventListener('change', function() {
        region_selector = this.value;
        if (sliding == true) {
            sliding = false;
            getRadarModelLinks();
            return false;
        }
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

function clearModelData() {
    for (const child of document.getElementById('radar-model-images').children) {
        child.style.opacity = "0"
        }
}

async function animate_radar_model_async() {
    enableForecastBrowser();
    await getRegions();
    await getModelData();
    await getNames();
    await getRadarModelLinks();
    enableRadarModelButtons();
}

function animate_radar_model_main() {
    animate_radar_model_async();
}