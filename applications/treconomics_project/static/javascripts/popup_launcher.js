/*
    Popup Launcher Script for Treconomics Experiments

    Author: David Maxwell
    Date: 2013-10-29
*/

COMPLETED_EXPERIMENT = false;

/*
Starts a new popup window pointing at the URL provided by parameter URL.
Width and height are optional parameters - 1024x768 is the default size of the popup if the parameters are not supplied.
*/
function launchPopup(url, width, height, topPos, leftPos) {
    topPos = (typeof topPos === 'undefined') ? ((screen.height / 2) - (height / 2)) : topPos;
    leftPos = (typeof leftPos === 'undefined') ? ((screen.width / 2) - (width / 2)) : leftPos;

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
        displayPopupFailed($('#instructions_text'));
    }
    else {
        var pollInterval = setInterval(function(){
            if (popup.closed) {
                if (COMPLETED_EXPERIMENT) {
                    displayCompletionMessage($('#instructions_text'));
                }
                else {
                    displayIncompleteMessage($('#instructions_text'));
                }

                clearInterval(pollInterval); // This should work as pollInterval will already be defined. Think about it...
            }
        }, 100);
    }
}

/*
Open a popup window displaying the search task the user must perform.
*/
function taskPopup(url) {
    launchPopup(url, 400, 600, 10, 10);
}

/*
Returns a boolean value indicating whether or not the browser being used has an active popup blocker.
Returns true if the function believes a popup window is present, and false if otherwise. Parameter popupReference is a reference to a popup window.
Solution adapted from http://davidwalsh.name/popup-block-javascript.
*/
function wasPopupBlocked(popupReference) {
    return (popupReference == null | typeof(popupReference) == 'undefined');
}

/*
Called when the user completes the experiment. Attempts to update text within the parent window, and close
the opened popup. Haha!
*/
function completeExperiment() {
    if (window.opener) {
        displayCompletionMessage(window.opener.$('#instructions_text'));
    }

    window.close();
}

/*
Displays the completion message to the user in the parent window.
Supply a reference to the JQuery object for element with ID instructions_text in the parent window.
 */
function displayCompletionMessage(instructionsElement) {
    instructionsElement.empty();
    instructionsElement.append(
        $('<div>Thank you very much for participating in this NewsSearch experiment!</div>')
            .attr({'style': 'text-align: center; font-size: 14pt; font-weight: bold;'}));
    instructionsElement.append(
        $('<div>Please let David know you have finished.</div>')
            .attr({'style': 'text-align: center; margin-top: 8px;'}));
}

function displayIncompleteMessage(instructionsElement) {
    instructionsElement.empty();
    instructionsElement.append(
        $('<div>You closed the experiment popup before completing.</div>')
            .attr({'style': 'text-align: center; font-size: 14pt; font-weight: bold; color: red;'}));
    instructionsElement.append(
        $('<div>Click <a href="#" onmouseup="launchPopup(popupURL, popupWidth, popupHeight);">here</a> to relaunch the popup window.</div>')
            .attr({'style': 'text-align: center; margin-top: 8px;'}));
}

function displayPopupFailed(instructionsElement) {
    instructionsElement.empty();
    instructionsElement.append(
        $('<div>You logged in successfully, but the experiment popup failed to launch automatically.</div>')
            .attr({'style': 'text-align: center; font-size: 14pt; font-weight: bold; color: red;'}));
    instructionsElement.append(
        $('<div>Your browser most likely blocked the popup from appearing. Click <a href="#" onmouseup="launchPopup(popupURL, popupWidth, popupHeight);">here</a> to launch the popup window manually.</div>')
            .attr({'style': 'text-align: center; margin-top: 8px;'}));
}