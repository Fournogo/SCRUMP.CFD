'use strict';

async function forecastLoader(link) {
    let response;
    for (let attempt = 0; attempt < 3; ++attempt) {
        if (attempt > 0) {
            console.log('Loading failed... Attempt #' + attempt)
            await delay(100);
        }
        try {
            response = await fetch(link);
            return response; // It worked
        } catch {

        }
    }
    // Out of retries
    throw new Error("Serious Loading Error");
}

async function getDailyForecast() {
    const forecast_link = city.daily_forecast
    document.getElementById('forecast-message-text').innerHTML = city.proper_name.toUpperCase() + ' WEATHER FORECAST';
    const response = await forecastLoader(forecast_link);
    const json_data = await response.json();
    const forecast_data_array = json_data.properties.periods;
    for (let i = 0; i < 14; i++) {
        document.getElementById('day-' + String(i + 1)).innerHTML = forecast_data_array[i].name;
        document.getElementById('tem-' + String(i + 1)).innerHTML = Math.round(forecast_data_array[i].temperature,2) + ' F';
        document.getElementById('dew-' + String(i + 1)).innerHTML = Math.round(forecast_data_array[i].dewpoint.value * 1.8 + 32,2) + ' F';

        if (forecast_data_array[i].name.includes('night') == true || forecast_data_array[i].name.includes('Night') == true) {
            document.getElementById('tem-' + String(i + 1)).style.color = '#393EFF';
        } else {
            document.getElementById('tem-' + String(i + 1)).style.color = '#FF3939';
        }

        if (forecast_data_array[i].probabilityOfPrecipitation.value == null || forecast_data_array[i].probabilityOfPrecipitation.value == 0) {
            document.getElementById('pre-' + String(i + 1)).innerHTML = '~0%';
        } else {
            document.getElementById('pre-' + String(i + 1)).innerHTML = forecast_data_array[i].probabilityOfPrecipitation.value + '%';
        }
    }
    if (forecast_data_array[0].probabilityOfPrecipitation.value == null || forecast_data_array[0].probabilityOfPrecipitation.value == 0) {
        document.getElementById('pre').innerHTML = '~0%';
    } else {
        document.getElementById('pre').innerHTML = forecast_data_array[0].probabilityOfPrecipitation.value + '%';
    }
}

async function getCurrentTemp() {
    const current_conditions_link = city.current_conditions
    const response = await forecastLoader(current_conditions_link);
    const json_data = await response.json();
    document.getElementById('tem').innerHTML = round(json_data.properties.temperature.value * 1.8 + 32,1) + ' F'
    document.getElementById('dew').innerHTML = round(json_data.properties.dewpoint.value * 1.8 + 32,1) + ' F'
}

function round(value, decimals) {
    return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

function forecast() {
    getDailyForecast()
    getCurrentTemp()
    };