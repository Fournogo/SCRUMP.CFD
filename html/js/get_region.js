let city;

async function getRegion(regions) {
    let urlParams = new URLSearchParams(window.location.search);
    let forecast_location = urlParams.get('region')
    city = regions[forecast_location]
    console.log(city)
    if (city == undefined) {
        city = regions['usa']
    }
    console.log(city)
    animate_goes_main();
    animate_radar_model_main();
};

fetch("json/regions.json")
.then(response => response.json())
.then(json => getRegion(json));