async function getCurrentUV() {
    const forecast_link = city.uv_daily;
    const response = await fetch(forecast_link);
    const json_data = await response.json();
    let uvi = json_data["0"].UV_INDEX;
    document.getElementById('currentuv').innerHTML = uvi;
};

function sun_fax() {
    getCurrentUV();
};