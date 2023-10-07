let city;
let region_selector;
let current_region_selection;

async function getCity(cities) {
    let urlParams = new URLSearchParams(window.location.search);
    let forecast_location = urlParams.get('city')
    console.log('CITIES:')
    console.log(cities)
    let region_list = [];
    for (let i = 0; i < cities.length; i++) {
        let region_option = document.createElement("option");

        if (forecast_location == cities[i].city) {
            city = cities[i]
            console.log('CITY:')
            console.log(city)
            region_option.selected = true;
            region_selector = city.model_state;
            current_region_selection = region_selector;

            for (const child of document.getElementById('region-selector').children) {
                if (child.innerHTML == city.proper_model_region) {
                    child.remove()
                }
            }

            region_list.push(cities[i].proper_model_region);
            region_option.text = cities[i].proper_model_region;
            region_option.value = cities[i].model_state;
            document.getElementById('region-selector').appendChild(region_option);
            continue
        }

        if (!(region_list.includes(cities[i].proper_model_region))) {
            region_list.push(cities[i].proper_model_region);
            region_option.text = cities[i].proper_model_region;
            region_option.value = cities[i].model_state;
            document.getElementById('region-selector').appendChild(region_option);
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