'use strict';

const sounding_url = 'https://www.spc.noaa.gov';

async function getSoundingLinks() {
    const response = await fetch('../goes/sounding/sounding_link.json');
    const json_data = await response.json();
    let code = city.sounding_code;
    let final_link = sounding_url + json_data[code];
    let element = document.createElement('img');
    element.src = final_link;
    document.getElementById('sounding').appendChild(element);
}

/*async function soundingMain() {
    await getSoundingLinks();
}*/

function soundingMain() {
    getSoundingLinks();
}