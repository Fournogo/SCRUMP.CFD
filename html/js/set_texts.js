'use-strict';

async function setTexts(json_data) {
    console.log(json_data)
    document.getElementById('radar-text').innerHTML = json_data[city.state][city.city].radar_temp;
    document.getElementById('goes-text').innerHTML = json_data[city.state][city.city].goes_satellite;
    document.getElementById('radar-model-text').innerHTML = json_data[city.state][city.city].radar_model;
    document.getElementById('sounding-text').innerHTML = json_data[city.state][city.city].sounding;
}

function set_texts() {
    fetch("json/city_texts.json")
    .then(response => response.json())
    .then(json => setTexts(json));
};
