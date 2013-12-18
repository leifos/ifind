/*
A little JavaScript file to make the show task popup disappear when the user ends the current task.
Avoids that little bit of confusion - gets rid of the popup automatically when it's no longer needed!

Author: David
*/

function checkPopupStatus() {
    var parentPath = window.opener.location.pathname;

    if (parentPath.indexOf('postpracticetask') != -1 || parentPath.indexOf('posttaskquestions') != -1) {
        self.close();
    }
}

// Every 500ms, check if the popup is still required. If it's not needed, it commits suicide.
setInterval(checkPopupStatus, 500);