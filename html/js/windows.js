let model_browser_open = false;
let model_is_max = false;
let model_is_min = false;

function setupWindows() {
    let main_elements = document.getElementsByClassName('overall-container')
    Array.from(main_elements).forEach((element) => {
        element.dataset.is_minimized = 'false';
        element.dataset.is_closed = 'false';
        element.dataset.window_size = 'normal';
        
        element.dataset.normal_width = element.clientWidth;
    });

    let vert_elements = document.getElementsByClassName('vertical-container')
    Array.from(vert_elements).forEach((element) => {
        element.dataset.normal_height = element.clientHeight;
    });

    let model_browser_button = document.getElementById('toggle-model-browser')
    model_browser_button.dataset.browser_open = 'false';
}

function closeWindow(element) {
    let parent_element = element.parentNode.parentNode;
    let content_element = parent_element.querySelector('.inside-stuff');
    
    /* Disabled until the menu is made
    parent_element.style.display = 'none';

    if (parent_element.dataset.window_size == 'max') {
        minMaxWindow(element)
    }

    if (parent_element.dataset.is_minimized == 'true') {
        minimizeWindow(element)
    }*/
}

function minMaxWindow(element) {
    let parent_element = element.parentNode.parentNode;
    let vertical_element = element.parentNode.parentNode.parentNode;
    let yellow_element = parent_element.querySelector('.inside-stuff')

    if (parent_element.dataset.is_minimized == 'true') {
        content_element.style.display = 'block';
        vertical_element.style.height = vertical_element.dataset.normal_height + 'px';
        parent_element.dataset.is_minimized = 'false';
        return false
    } 
    
    if (parent_element.dataset.window_size == 'normal') {
        parent.document.getElementById('back-button').style.display = 'none';
        parent.document.getElementById('music-button').style.display = 'none';
        document.body.style.overflow = 'hidden';
        parent_element.style.width = '100%';
        vertical_element.style.position = 'fixed';
        vertical_element.style.height = '100vh';
        parent_element.style.zIndex = '200';
        vertical_element.style.zIndex = '200';
        vertical_element.style.margin = '0';
        parent_element.dataset.window_size = 'max';
        document.getElementById('model-menu').style.position = 'fixed';

    } else if (parent_element.dataset.window_size == 'max') {
        parent.document.getElementById('back-button').style.display = 'block';
        parent.document.getElementById('music-button').style.display = 'block';

        document.body.style.overflow = 'auto';

        vertical_element.style.position = 'relative';
        parent_element.style.width = parent_element.dataset.normal_width + 'px';

        vertical_element.style.height = vertical_element.dataset.normal_height + 'px';
        parent_element.style.zIndex = '5';
        vertical_element.style.zIndex = '5';
        vertical_element.style.marginTop = '40px';
        vertical_element.style.marginBottom = '40px';
        parent_element.style.marginLeft = 'auto';
        parent_element.style.marginRight = 'auto';
        parent_element.dataset.window_size = 'normal';
        document.getElementById('model-menu').style.position = 'absolute';
    }
}

function minimizeWindow(element) {
    let parent_element = element.parentNode.parentNode;
    let vertical_element = element.parentNode.parentNode.parentNode;
    let content_element = parent_element.querySelector('.inside-stuff')

    if (parent_element.dataset.window_size = 'max') {
        parent.document.getElementById('back-button').style.display = 'block';
        parent.document.getElementById('music-button').style.display = 'block';

        document.body.style.overflow = 'auto';

        vertical_element.style.position = 'relative';
        parent_element.style.width = parent_element.dataset.normal_width + 'px';
        vertical_element.style.height = vertical_element.dataset.normal_height + 'px';
        parent_element.style.zIndex = '5';
        vertical_element.style.zIndex = '5';
        vertical_element.style.marginTop = '40px';
        vertical_element.style.marginBottom = '40px';
        parent_element.style.marginLeft = 'auto';
        parent_element.style.marginRight = 'auto';
        parent_element.dataset.window_size = 'normal';
    }

    if (parent_element.dataset.is_minimized == 'false') {
        content_element.style.display = 'none';
        vertical_element.style.height = '30px';
        parent_element.style.width = parent_element.dataset.normal_width + 'px';
        parent_element.dataset.is_minimized = 'true';

    } else if (parent_element.dataset.is_minimized == 'true') {
        content_element.style.display = 'block';
        vertical_element.style.height = vertical_element.dataset.normal_height + 'px';
        parent_element.dataset.is_minimized = 'false';
    }

    
}

function maximizeModel() {
    let model_container = document.getElementById('radar-model-cont');
    let model_browser = document.getElementById('model-menu');
    let vert_container = document.getElementById('radar-model-vert');

    parent.document.getElementById('back-button').style.display = 'none';
    parent.document.getElementById('music-button').style.display = 'none';

    vert_container.style.height = '100vh';
    vert_container.style.position = 'fixed';
    model_container.style.position = 'fixed';
    model_browser.style.position = 'fixed';
    vert_container.style.zIndex = '20';
    model_browser.style.height = '100vh';

    vert_container.style.marginTop = '0';
    vert_container.style.marginBottom = '0';

    document.body.style.overflow = 'hidden';

    if (model_browser_open == false) {
        model_container.style.width = '100%';
    } else {
        model_container.style.width = '75%';
    }

    model_is_max = true;
}

function normalizeModel() {
    let model_container = document.getElementById('radar-model-cont');
    let model_browser = document.getElementById('model-menu');
    let vert_container = document.getElementById('radar-model-vert');
    let yellow_part = document.getElementById('model-inside');

    let default_width = model_container.dataset.normal_width + 'px';
    let default_height = vert_container.dataset.normal_height + 'px';

    parent.document.getElementById('back-button').style.display = 'block';
    parent.document.getElementById('music-button').style.display = 'block';

    document.body.style.overflow = 'auto';

    vert_container.style.marginTop = '40px';
    vert_container.style.marginBottom = '40px';

    yellow_part.style.display = 'block';
    vert_container.style.height = default_height;
    vert_container.style.position = 'relative';
    model_browser.style.height = '100%';
    vert_container.style.zIndex = '5';
    model_container.style.position = 'relative';
    model_browser.style.position = 'absolute';

    if (model_browser_open == false) {
        model_container.style.width = default_width;
        model_container.style.position = 'relative';
    } else {
        model_container.style.width = '75%';
        model_container.style.position = 'absolute';
    }

    model_is_max = false;
    model_is_min = false;
}

function minimizeModel() {
    normalizeModel()
    closeModelBrowser()
    let model_container = document.getElementById('radar-model-cont');
    let model_browser = document.getElementById('model-menu');
    let vert_container = document.getElementById('radar-model-vert');
    let yellow_part = document.getElementById('model-inside');
    vert_container.style.height = '30px';
    yellow_part.style.display = 'none';
    model_browser.style.display = 'none';
    model_is_min = true;
}

function openModelBrowser() {
    let model_browser = document.getElementById('model-menu');
    let model_container = document.getElementById('radar-model-cont');

    model_browser.style.display = 'block';
    model_container.style.width = '75%';

    if (model_is_max == false) {
        model_container.style.position = 'absolute';
    }

    model_browser_open = true;
}

function closeModelBrowser() {
    let model_browser = document.getElementById('model-menu');
    let model_container = document.getElementById('radar-model-cont');

    let default_width = model_container.dataset.normal_width + 'px';

    model_browser.style.display = 'none';

    if (model_is_max == true) {
        model_container.style.width = '100%';
    } else {
        model_container.style.width = default_width;
        model_container.style.position = 'relative';
    }

    model_browser_open = false;
}

function minMaxModel() {
    if (model_is_max == true) {
        normalizeModel()
    } else if (model_is_min == true) {
        normalizeModel()
    } else {
        maximizeModel()
    }
}

function openCloseBrowser() {
    if (model_browser_open == true) {
        closeModelBrowser()
    } else {
        openModelBrowser()
    }
}

function minModel() {
    if (model_is_min == true) {
        normalizeModel()
    } else {
        minimizeModel()
    }
}