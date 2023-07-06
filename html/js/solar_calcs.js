//ALL THIS CODE WAS 'WRITTEN' BY ME BUT REALLY TAKEN FROM A NOAA SPREADSHEET USED TO CALCULATE SUNRISE AND SUNSET; WHICH IS ALSO
//BASED ON APPROXIMATIONS PRODUCED BY NASA'S JPL AND THEIR HORIZONS SYSTEM. THIS TRULY APPROXIMATES THE ORBITAL POSITION OF EARTH
//AND THE SUN FOR THE GIVEN TIME AND THEN SOLVES FOR THE ANGLES FOR AN OBSERVER ON EARTH WHICH IS PRETTY CRAZY TBH

function degreesToRadians(degrees) {
  return degrees * (Math.PI / 180);
}

function radiansToDegrees(radians) {
  return radians * (180 / Math.PI)
}

function getJulian(date) {
    return (date / 86400000) + 2440587.5;
  }

// IMPORTANT GLOBALS
let sunrise_decimal_utc;
let sunset_decimal_utc;
let sun_declination_deg;

function solar_calcs_main() {

  // IMPORTANT INFORMATION FOR LOCATING THE OBSERVER
  let obs_latitude = city.coordinates[0]
  let obs_longitude = city.coordinates[1]

  let today = new Date();
  today.setHours(12, 0, 0, 0)
    
  console.log(today)
  let julian = getJulian(today);
  console.log(julian);

  let julian_century = (julian - 2451545) / 36525;
  let geom_mean_long_sun_deg = 280.46646 + julian_century * (36000.76983 + julian_century * 0.0003032) % 360;
  let geom_mean_anom_sun_deg = 357.52911 + julian_century * (35999.05029 - 0.0001537 * julian_century);

  let geom_mean_long_sun_rad = degreesToRadians(geom_mean_long_sun_deg);
  let geom_mean_anom_sun_rad = degreesToRadians(geom_mean_anom_sun_deg);

  let earth_eccent = 0.016708634 - julian_century * (0.000042037 + 0.0000001267 * julian_century);
  let sun_eq_ctr = Math.sin(geom_mean_anom_sun_rad) * (1.914602 - julian_century * (0.004817 + 0.000014 * julian_century));
  + Math.sin(2 * geom_mean_anom_sun_rad) * (0.019993-0.000101 * julian_century);
  + Math.sin(3 * geom_mean_anom_sun_rad) * 0.000289;

  let sun_true_long_deg = geom_mean_long_sun_deg + sun_eq_ctr;
  //let sun_true_anom_deg = geom_mean_anom_sun_deg + sun_eq_ctr;

  //let sun_true_long_rad = degreesToRadians(sun_true_long_deg);
  //let sun_true_anom_rad = degreesToRadians(sun_true_anom_deg);

  //let sun_rad_vector = (1.000001018 * (1 - earth_eccent ** 2)) / (1 + earth_eccent * Math.cos(sun_true_anom_rad));

  let sun_app_long_deg = sun_true_long_deg - 0.00569 - 0.00478 * Math.sin(degreesToRadians(125.04 - 1934.136 * julian_century));
  let sun_app_long_rad = degreesToRadians(sun_app_long_deg);
  let mean_obl_ecliptic_deg = 23 + (26 + ((21.448 - julian_century * (46.815 + julian_century * (0.00059 - julian_century * 0.001813)))) / 60) / 60;

  let obl_corr_deg = mean_obl_ecliptic_deg + 0.00256 * Math.cos(degreesToRadians(125.04-1934.136 * julian_century));
  let obl_corr_rad = degreesToRadians(obl_corr_deg);

  //let sun_rt_ascen_rad = Math.atan2(Math.cos(sun_app_long_rad), Math.cos(obl_corr_rad) * Math.sin(sun_app_long_rad));
  //let sun_rt_ascen_deg = radiansToDegrees(sun_rt_ascen_rad);

  //SUN DECLINATION IN DEGREES
  let sun_declination_rad = Math.asin(Math.sin(obl_corr_rad) * Math.sin(sun_app_long_rad));
  sun_declination_deg = radiansToDegrees(sun_declination_rad);

  let var_y = Math.tan(obl_corr_rad / 2) ** 2

  let eq_of_time_min = 4 * radiansToDegrees(
    var_y * Math.sin(2 * geom_mean_long_sun_rad) 
    - 2 * earth_eccent * Math.sin(geom_mean_anom_sun_rad) 
    + 4 * earth_eccent * var_y * Math.sin(geom_mean_anom_sun_rad) * Math.cos(2 * geom_mean_long_sun_rad)
    - 0.5 * var_y * var_y * Math.sin(4 * geom_mean_long_sun_rad)
    - 1.25 * earth_eccent * earth_eccent * Math.sin(2 * geom_mean_anom_sun_rad)
  );

  let HA_sunrise_deg = radiansToDegrees(
    Math.acos(Math.cos(degreesToRadians(90.833)) / (Math.cos(degreesToRadians(obs_latitude)) * Math.cos(sun_declination_rad)) - Math.tan(degreesToRadians(obs_latitude)) * Math.tan(sun_declination_rad))
  );

  let solar_noon_decimal_utc = (720 - 4 * obs_longitude - eq_of_time_min) / 1440;
  console.log(solar_noon_decimal_utc)
  //SUNRISE AND SUNSET IN DECIMALS
  sunrise_decimal_utc = (solar_noon_decimal_utc - HA_sunrise_deg * 4/1440);
  sunset_decimal_utc = (solar_noon_decimal_utc + HA_sunrise_deg * 4/1440);

  let max_sun_angle = 90 - Math.abs(obs_latitude) + sun_declination_deg;
  document.getElementById('sun-angle').innerHTML = max_sun_angle.toFixed(2) + '°';

};