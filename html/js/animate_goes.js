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
let goes_current_animation_length = 8;

let goes_length_selector = 8;
let goes_speed = 10;

let goes_is_latest = false;

let goes_json_file;
let goes_number_iamges_loaded = 0;

async function getGoesLinks() {
    enableGoesLoading();
    const response = await fetch(city.goes_json);
    goes_json_file = await response.json();
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function decodeHandler(element) {
    for (let attempt = 0; attempt < 10; ++attempt) {
        if (attempt > 0) {
            console.log('Decode failed... Attempt #' + attempt)
            await delay(100);
        }
        try {

            await element.decode();
            return; // It worked
        } catch {
        }
    }
    // Out of retries
    throw new Error("Serious Decoding Error");
}

async function updateGoesLinks() {
    enableGoesLoading();
    let percent_increment = (1 / number_of_goes_images);
    //let percent_complete = 0 + document.getElementById('goes-images').children.length / number_of_goes_images;
    let percent_complete = (goes_number_iamges_loaded / number_of_goes_images)
    let percent_complete_rounded = ((Math.round(percent_complete * 1000) / 1000) * 100).toFixed(1)
    document.getElementById('goes-images').innerHTML = '';
    let goes_temp_image_array = [];
    document.getElementById('goes-nyancat').style.left = (percent_complete_rounded + "%");
    document.getElementById('goes-loading-percent').innerText = ("LOADING: " + percent_complete_rounded + "%" + " COMPLETE");
    goes_animation_index = 0
    next_goes_animation_index = goes_animation_index;
    let link;
    let final_link;
    let element;
    let image_links;
    if (city.state != 'national') {
        image_links = goes_json_file.images["1200x1200"];
    } else if (city.state == 'national') {
        image_links = goes_json_file.images["2500x1500"];
    }

    for (let i = 0; i < (number_of_goes_images - goes_number_iamges_loaded); i++) {
        link = image_links[image_links.length - number_of_goes_images + i - 1];
        final_link = city.goes_link + link;
        element = document.createElement('img');
        element.src = final_link;

        await decodeHandler(element);

        if (i == 0) {
            element.style.opacity = "1";
        } else {
            element.style.opacity = "0";
        }
        document.getElementById('goes-images').append(element);
        goes_temp_image_array.push(element);

        percent_complete += percent_increment;
        percent_complete_rounded = ((Math.round(percent_complete * 1000) / 1000) * 100).toFixed(1)
        document.getElementById('goes-nyancat').style.left = (percent_complete_rounded + "%");
        document.getElementById('goes-loading-percent').innerText = ("LOADING: " + percent_complete_rounded + "%" + " COMPLETE");
    }

    for (const element of goes_image_array) {
        document.getElementById('goes-images').append(element);
    }

    goes_image_array = goes_temp_image_array.concat(goes_image_array)
    clearGoesLoading();
    goes_number_iamges_loaded = goes_image_array.length;
    goes_animation_paused = false;
    goes_animation_unpaused = true;
    goes_pause_is_clicked = false;
    animateGoes();
}

function clearGoes() {
    for (const child of document.getElementById('goes-images').children) {
        child.style.opacity = "0"
      }
}

function animateGoes() { 
    let goes_animation_delay;

    if (goes_current_animation_length != goes_length_selector) {
        goes_current_animation_length = goes_length_selector;
        if (goes_number_iamges_loaded < goes_current_animation_length * 12) {
            number_of_goes_images = goes_current_animation_length * 12;
            goes_minimum_index = 0;
            goes_animation_index = 0;
            next_goes_animation_index = 0;
            clearGoes();
            updateGoesLinks();
            return false;
        } else {
            goes_minimum_index = (number_of_goes_images - goes_current_animation_length * 12);
            goes_animation_index = goes_minimum_index;
            next_goes_animation_index = goes_animation_index;
            clearGoes();
            goes_image_array[goes_minimum_index].style.opacity = "1";
        }
    }

    if (goes_next_is_clicked == true) {
        goes_animation_paused = true;
        goes_next_is_clicked = false;
        next_goes_animation_index = goes_animation_index + 1;
    }

    if (goes_back_is_clicked == true) {
        goes_animation_paused = true;
        goes_back_is_clicked = false;
        next_goes_animation_index = goes_animation_index - 1;
    }

    if (goes_animation_index == goes_minimum_index) {
        goes_image_array[goes_image_array.length - 1].style.opacity = "0";
        goes_image_array[goes_animation_index].style.opacity = "1";
        goes_image_array[goes_animation_index + 1].style.opacity = "0";
        if (goes_animation_paused == false) {
            next_goes_animation_index = goes_animation_index + 1;
            goes_animation_delay = 1000 / goes_speed;
        } else {
            goes_animation_delay = 100;
        }

    } else if (goes_animation_index == goes_image_array.length - 1) {
        goes_image_array[goes_animation_index - 1].style.opacity = "0";
        goes_image_array[goes_animation_index].style.opacity = "1";
        goes_image_array[goes_minimum_index].style.opacity = "0";
        if ((goes_is_latest == true) && (goes_animation_paused == false)) {
            next_goes_animation_index = goes_minimum_index;
            goes_is_latest = false;
            goes_animation_delay = 100;
        } else if (goes_animation_paused == false) {
            next_goes_animation_index = goes_minimum_index;
            goes_animation_delay = 20000 / goes_speed;
        } else {
            goes_animation_delay = 100;
        }
        

    } else {
        goes_image_array[goes_animation_index - 1].style.opacity = "0";
        goes_image_array[goes_animation_index].style.opacity = "1";
        goes_image_array[goes_animation_index + 1].style.opacity = "0";
        if (goes_animation_paused == false) {
            next_goes_animation_index = goes_animation_index + 1;
            goes_animation_delay = 1000 / goes_speed;
        } else {
            goes_animation_delay = 100;
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
    
    document.getElementById('goes-images').style.cursor = "pointer";

    document.getElementById('goes-images').addEventListener("click", function() {
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

    document.getElementById('goes-last-button').addEventListener("click", function() {
        clearGoes();
        goes_animation_paused = true;
        goes_animation_index = goes_image_array.length - 1;
        goes_image_array[goes_animation_index].style.opacity = "1";
        next_goes_animation_index = goes_animation_index
        goes_is_latest = true;
    });

    document.getElementById('goes-speed-select').addEventListener('change', function() {
        goes_speed = Number(this.value);
      });

    document.getElementById('goes-time-select').addEventListener('change', function() {
        goes_length_selector = Number(this.value);
    });

}

function clearGoesLoading() {
    document.getElementById('goes-images').style.cursor = "pointer";
    document.getElementById('goes-loading-text').style.opacity = "0";
    document.getElementById('goes-loading-text').style.zIndex = "-1";
}

function enableGoesLoading() {
    document.getElementById('goes-images').style.cursor = "auto";
    document.getElementById('goes-loading-text').style.opacity = "1";
    document.getElementById('goes-loading-text').style.zIndex = "10";
}

async function animate_goes_async() {
    await getGoesLinks();
    await updateGoesLinks();
    enableGoesButtons();
}

function animate_goes_main() {
    animate_goes_async();
}