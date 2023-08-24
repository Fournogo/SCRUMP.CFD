let city;

async function getCity(cities) {
    let urlParams = new URLSearchParams(window.location.search);
    let forecast_location = urlParams.get('city')
    console.log('CITIES:')
    console.log(cities)
    for (let i = 0; i < cities.length; i++) {

        if (forecast_location == cities[i].city) {
            city = cities[i]
            console.log('CITY:')
            console.log(city)
        }
    }

    if (city == null) {
        city = cities[0]
    }

    solar_calcs_main();
    hourly();
    radar();
    forecast();
    soundingMain();
    animate_goes_main();
    animate_radar_model_main();
    set_texts();
    getCurrentUV();
    setupWindows();
};

fetch("json/cities.json")
.then(response => response.json())
.then(json => getCity(json.cities));