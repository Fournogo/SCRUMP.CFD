
function setupWindows() {
    let main_elements = document.getElementsByClassName('overall-container')
    Array.from(main_elements).forEach((element) => {
        element.dataset.is_minimized = 'false';
        element.dataset.is_closed = 'false';
        element.dataset.window_size = 'normal';
        
        element.dataset.normal_height = element.clientHeight;
        element.dataset.normal_width = element.clientWidth;

        console.log(element.dataset)
    });
}

function closeWindow(element) {
    let parent_element = element.parentNode.parentNode;
    let content_element = parent_element.querySelector('.yellow-rectangle');
    
    parent_element.style.display = 'none';

    if (parent_element.dataset.window_size == 'max') {
        minMaxWindow(element)
    }

    if (parent_element.dataset.is_minimized == 'true') {
        minimizeWindow(element)
    }
}

function minMaxWindow(element) {
    let parent_element = element.parentNode.parentNode;
    let content_element = parent_element.querySelector('.yellow-rectangle')

    if (parent_element.dataset.is_minimized == 'true') {
        content_element.style.display = 'block';
        parent_element.style.height = parent_element.dataset.normal_height + 'px';
        parent_element.dataset.is_minimized = 'false';
        return false
    } 
    
    if (parent_element.dataset.window_size == 'normal') {
        parent.document.getElementById('back-button').style.display = 'none';
        parent.document.getElementById('music-button').style.display = 'none';

        document.body.style.overflow = 'hidden';

        parent_element.style.position = 'fixed';
        parent_element.style.width = '100%';
        parent_element.style.height = '100vh';
        parent_element.style.zIndex = '200';
        parent_element.style.margin = '0';
        parent_element.dataset.window_size = 'max';

    } else if (parent_element.dataset.window_size == 'max') {
        parent.document.getElementById('back-button').style.display = 'block';
        parent.document.getElementById('music-button').style.display = 'block';

        document.body.style.overflow = 'auto';

        parent_element.style.position = 'relative';
        parent_element.style.width = parent_element.dataset.normal_width + 'px';
        parent_element.style.height = parent_element.dataset.normal_height + 'px';
        parent_element.style.zIndex = '5';
        parent_element.style.marginTop = '40px';
        parent_element.style.marginBottom = '40px';
        parent_element.dataset.window_size = 'normal';
    }
}

function minimizeWindow(element) {
    let parent_element = element.parentNode.parentNode;
    let content_element = parent_element.querySelector('.yellow-rectangle')

    if (parent_element.dataset.is_minimized == 'false') {
        content_element.style.display = 'none';
        parent_element.style.height = '30px';
        parent_element.style.width = parent_element.dataset.normal_width + 'px';
        parent_element.dataset.is_minimized = 'true';

    } else if (parent_element.dataset.is_minimized == 'true') {
        content_element.style.display = 'block';
        parent_element.style.height = parent_element.dataset.normal_height + 'px';
        parent_element.dataset.is_minimized = 'false';
    }

    
}