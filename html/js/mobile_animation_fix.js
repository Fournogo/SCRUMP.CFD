/*let iframe = document.getElementById('main-frame');
let innerDoc = iframe.contentDocument || iframe.contentWindow.document;
*/
let observer_options = {
    root: document.querySelector("#main-frame"),
    rootMargin: "0px",
    threshold: 0.999,
  };

let radar_model_target = document.querySelector('#radar-model-cont');
let goes_target = document.querySelector('#goes-image-cont');

let radar_model_observer = new IntersectionObserver(checkRadarModelVis, observer_options);
let goes_observer = new IntersectionObserver(checkGoesVis, observer_options);

function checkRadarModelVis(entries) {
    console.log('RADAR MODEL EMERGENCY PAUSE')
    const [entry] = entries;
    if (entry.isIntersecting == false) {
        radar_model_animation_paused = true;
    } else {
        radar_model_animation_paused = false;
    }

}

function checkGoesVis(entries) {
    const [entry] = entries;
    console.log('GOES EMERGENCY PAUSE')
    if (entry.isIntersecting == false) {
        goes_animation_paused = true;
    } else {
        goes_animation_paused = false;
    }
}

if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/.test(navigator.userAgent)) {
    radar_model_observer.observe(radar_model_target)
    goes_observer.observe(goes_target)
}

//setInterval(checkGoesVis, 1000);