/*
    Popup Launcher Script for Treconomics Experiments

    Author: David Maxwell
    Date: 2013-10-29
*/

/*
Starts a new popup window pointing at the URL provided by parameter URL.
Width and height are optional parameters - 1024x768 is the default size of the popup if the parameters are not supplied.
*/
function launchPopup(url, width, height) {
    var topPos = (screen.height / 2) - (height / 2);
    var leftPos = (screen.width / 2) - (width / 2);

    if (typeof width === 'undefined') {
        width = 1024;
    }

    if (typeof height === 'undefined') {
        height = 768;
    }

    var popup = window.open(url,
            'Treconomics Experiment',
            'toolbar=no,' +
                    'location=no,' +
                    'directories=no,' +
                    'status=no,' +
                    'menubar=no,' +
                    'scrollbars=no,' +
                    'resizable=no,' +
                    'copyhistory=no,' +
                    'width='+ width +',' +
                    'height='+ height +',' +
                    'top='+ topPos +',' +
                    'left='+ leftPos);

    if (wasPopupBlocked(popup)) {
        alert("The popup failed to launch. Please try starting the experiment by clicking on the link.");
    }
}

/*
Returns a boolean value indicating whether or not the browser being used has an active popup blocker.
Returns true if the function believes a popup window is present, and false if otherwise. Parameter popupReference is a reference to a popup window.
Solution adapted from http://davidwalsh.name/popup-block-javascript.
*/
function wasPopupBlocked(popupReference) {
    return (popupReference == null | typeof(popupReference) == 'undefined');
}

function completeExperiment() {
    if (window.opener) {
        window.opener.$('#instructions_text').empty();
        window.opener.$('#instructions_text').append(
            $('<div>Thank you very much for participating in this Treconomics experiment!</div>')
                .attr({'style': 'text-align: center; font-size: 14pt; font-weight: bold;'}));
    }

    window.close();
}