'use strict';

let path_to_sky = '../json/sky_cover_data.json'

let temperatures = ["Temperature"];
let precip_probs = ["Precip"];
let dewpoints = ["Dewpoint"];
let humidity = ["Humidity"];
let uvi = ["UVI"];
let uv_times = ["x"];
let forecast_time = ["x"];
let chart_data_temp_dew = [];
let chart_data_precip = [];
let chart_data_uv = [];
let chart_data_sky = [];
let is_daytime = ["Daytime"];
let region_list = [];
let sky_cover = ["Sky Cover"]
let sky_cover_times = ["x"]

document.addEventListener("DOMContentLoaded", (event) => {
    console.log("DOM fully loaded and parsed");
  });

// PLOT TEMP AND DEWPOINT 
function plotTemp() {
    chart_data_temp_dew.push(forecast_time);
    chart_data_temp_dew.push(temperatures);
    chart_data_temp_dew.push(dewpoints);

    // GENERATE HOURLY TEMP AND DEWPOINT GRAPH
    bb.generate({
        title: {
            text: "Estimated Hourly Temperature and Dewpoint"
          },
        data: {
            x: "x",
            xLocaltime: true,
            xFormat: "%Y-%m-%d %H:%M",
            columns: chart_data_temp_dew,
            types: {
              Temperature: "line",
              Dewpoint: "line"
            },
            colors: {
              Temperature: "red",
              Dewpoint: "green"
            }
        },
        axis: {
            x: {
                type: "timeseries",
                tick: {
                    format: function (x) {
                        let hours = x.getHours(); 
                        let ampm = hours >= 12 ? 'PM' : 'AM';
                        hours = hours % 12 || 12;
                        let month = x.getMonth() + 1; // Get the month value (January is 0)
                        let date = x.getDate(); // Get the date value
                        return month + "-" + date + " " + hours + ":00 " + ampm;
                    }
              }
            }
          },
        regions: region_list,
        grid: {
            y: {
              show: true
            }
        },
        bindto: "#chart"
    });

}

// PLOT PRECIP
function plotPrecip() {

    chart_data_precip.push(forecast_time);
    chart_data_precip.push(humidity);
    chart_data_precip.push(precip_probs);

    // GENERATE PRECIP PROB GRAPH
    bb.generate({
        title: {
            text: "Estimated Probability of Precipitation & Relative Humdity"
          },
        data: {
            x: "x",
            xLocaltime: true,
            xFormat: "%Y-%m-%d %H:%M",
            columns: chart_data_precip,
            types: {
                Humidity: "line",
                Precip: "line"
            },
            colors: {
                Humidity: "green",
                Precip: "blue"
            }
        },
        axis: {
            y: {
                max: 100,
                min: 0,
                tick: {
                    values: [0,10,20,30,40,50,60,70,80,90,100]
                }
              },
            x: {
                type: "timeseries",
                tick: {
                    format: function (x) {
                        let hours = x.getHours(); 
                        let ampm = hours >= 12 ? 'PM' : 'AM';
                        hours = hours % 12 || 12;
                        let month = x.getMonth() + 1; // Get the month value (January is 0)
                        let date = x.getDate(); // Get the date value
                        return month + "-" + date + " " + hours + ":00 " + ampm;
                    }
              },
            }
          },
          regions: region_list,
          grid: {
            y: {
              show: true
            }
          },
        bindto: "#chart2"
    });
}

// PLOT UV INDEX
function plotUV() {

    chart_data_uv.push(uv_times);
    chart_data_uv.push(uvi);

    // GENERATE UV INDEX GRAPH
    bb.generate({
        title: {
            text: "Estimated UV Index"
          },
        data: {
            x: "x",
            xLocaltime: true,
            xFormat: "%Y-%m-%d %H:%M",
            columns: chart_data_uv,
            types: {
                UVI: "line",
            },
            colors: {
                UVI: "red"
            }
        },
        axis: {
            y: {
                max: 13,
                min: 0,
                tick: {
                    values: [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
                }
              },
            x: {
                type: "timeseries",
                tick: {
                    format: function (x) {
                        let hours = x.getHours(); 
                        let ampm = hours >= 12 ? 'PM' : 'AM';
                        hours = hours % 12 || 12;
                        let month = x.getMonth() + 1; // Get the month value (January is 0)
                        let date = x.getDate(); // Get the date value
                        return month + "-" + date + " " + hours + ":00 " + ampm;
                    }
              }
            }
          },
          regions: region_list,
          grid: {
            y: {
              show: true
            }
          },
        bindto: "#chart3"
    });

}

// PLOT SKY COVER
function plotSky() {
    chart_data_sky.push(sky_cover_times);
    chart_data_sky.push(sky_cover);

    // GENERATE SKY GRAPH
    bb.generate({
        title: {
            text: "Estimated Percentage of Sky Covered by Clouds"
          },
        data: {
            x: "x",
            xLocaltime: true,
            xFormat: "%Y-%m-%d %H:%M",
            columns: chart_data_sky,
            types: {
                'Sky Cover': "line"
            },
            colors: {
                'Sky Cover': "blue"
            }
        },
        axis: {
            y: {
                max: 100,
                min: 0,
                tick: {
                    values: [0,10,20,30,40,50,60,70,80,90,100]
                }
              },
            x: {
                type: "timeseries",
                tick: {
                    format: function (x) {
                        let hours = x.getHours(); 
                        let ampm = hours >= 12 ? 'PM' : 'AM';
                        hours = hours % 12 || 12;
                        let month = x.getMonth() + 1; // Get the month value (January is 0)
                        let date = x.getDate(); // Get the date value
                        return month + "-" + date + " " + hours + ":00 " + ampm;
                    }
              },
            }
          },
          regions: region_list,
          grid: {
            y: {
              show: true
            }
          },
        bindto: "#point-chart"
    });
}

async function chartLoader(link) {
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

// GET HOURLY FORECAST DATA
async function getHourlyForecast() {
    const forecast_link = city.hourly_forecast;
    const response = await chartLoader(forecast_link);
    const json_data = await response.json();
    const forecast_data_array = json_data.properties.periods;
    for (let i = 0; i < 108; i++) {
        temperatures.push(forecast_data_array[i].temperature);
        dewpoints.push(forecast_data_array[i].dewpoint.value * 1.8 + 32);
        humidity.push(forecast_data_array[i].relativeHumidity.value);
        forecast_time.push(forecast_data_array[i].endTime.slice(0,10) + " " + forecast_data_array[i].endTime.slice(11,16));
        is_daytime.push(forecast_data_array[i].isDaytime);
        if (forecast_data_array[i].probabilityOfPrecipitation.value == null) {
            precip_probs.push(0)
        } else {
            precip_probs.push(forecast_data_array[i].probabilityOfPrecipitation.value)
        }
    }
    plotTemp();
    plotPrecip();
}

// GET THE CLOUD COVER FORECAST
async function getSkyCoverForecast() {
    const response = await chartLoader(path_to_sky);
    const json_data = await response.json();
    const sky_cover_data = json_data[city.city];

    for (let i = 0; i < 36; i++) {
        sky_cover.push(sky_cover_data[i][1]);
        sky_cover_times.push(sky_cover_data[i][0].slice(0,10) + " " + sky_cover_data[i][0].slice(11,16));
    }
    plotSky();
}

// GET UV FORECAST DATA
async function getUVForecast() {
    const forecast_link = city.uv_hourly;
    const response = await chartLoader(forecast_link);
    const json_data = await response.json();

    let uv_time;
    
    for (let i = 0; i < json_data.length; i++) {
        uvi.push(json_data[i].UV_VALUE)
        uv_time = EPA2Date(json_data[i].DATE_TIME)
        //uv_time = uv_time.toISOString("en-US", {timeZone: city.timezone});
        uv_times.push(uv_time);
    }
    plotUV();
}

// FIGURE OUT WHAT REGIONS TO SHADE ON THE GRAPHS
async function getShadedRegions() {
    let sunrise_time = new Date();
    let sunset_time = new Date();

    sunrise_time.setUTCHours(0,0,0,0)
    sunset_time.setUTCHours(0,0,0,0)

    let sunrise_day = Math.trunc(sunrise_decimal_utc)
    let sunset_day = Math.trunc(sunset_decimal_utc)

    sunrise_time.setUTCMilliseconds((sunrise_decimal_utc - sunrise_day) * 86400000)
    sunset_time.setUTCMilliseconds((sunset_decimal_utc - sunset_day) * 86400000)

    console.log(sunset_time);
    console.log(sun_declination_deg);
    //sunrise_time = new Date(sunrise_time);
    //sunset_time = new Date(sunset_time);
    let sunrise_local;
    let sunset_local;

    sunrise_local = sunrise_time.toLocaleTimeString("en-US", {timeZone: city.timezone});
    sunset_local = sunset_time.toLocaleTimeString("en-US", {timeZone: city.timezone});

    document.getElementById('sunrise').innerHTML = sunrise_local;
    document.getElementById('sunset').innerHTML = sunset_local;

    let daylight = new Date(null);
    daylight.setMilliseconds(sunset_time - sunrise_time);
    daylight = daylight.toISOString().slice(11,19);
    document.getElementById('day-length').innerHTML = daylight;

    sunrise_time.setDate(sunrise_time.getDate() - 1);
    sunset_time.setDate(sunset_time.getDate() - 2);

    for (let i = 0; i < 6; i++) {
        sunrise_time.setDate(sunrise_time.getDate() + 1);
        sunset_time.setDate(sunset_time.getDate() + 1);

        sunrise_local = sunrise_time.toISOString("en-US", {timeZone: city.timezone});
        sunset_local = sunset_time.toISOString("en-US", {timeZone: city.timezone});

        region_list.push({'start': sunset_local, 'end': sunrise_local})
    }
    console.log(region_list)
}

// FIX THE DATES PROVIDED BY THE EPA
function EPA2Date (EPAdate) {
    let month;
    let hour;
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for (let i = 0; i < months.length; i++) {
        if (months[i] == EPAdate.slice(0,3)) {
            month = i;
        }
    }
    const day = EPAdate.slice(4,6);
    const year = EPAdate.slice(7,11);

    if (EPAdate.slice(15) == 'PM' && EPAdate.slice(12,14) != '12') {
        hour = Number(EPAdate.slice(12,14)) + 12;
    } else if (EPAdate.slice(15) == 'AM' && EPAdate.slice(12,14) == '12'){
        hour = 0
    } else {
        hour = EPAdate.slice(12,14);
    }
    let date = new Date(year, month, day, hour)
    return date
}

// GET ER DONE
async function hourly_main() {
    await getShadedRegions();
    getHourlyForecast();
    getUVForecast();
    getSkyCoverForecast();
}

function hourly() {
    hourly_main();
}