/*

Search Helpers for NewsSearch - used for all types of search.

Author: David Maxwell
Date: 2013-11-13
Revision: 1

*/

var INTERFACE_ENABLED = true;

function disableClick(event) {
    if (event.button==2) {
        return false;
    }
}

$(function() {
    bindDocumentClicks();
    bindResultHovering();
    bindFormSubmit();

    if ($('#query')) {
        $('#query').focus();
    }

    $('.searchbox, .smallsearchbox').keypress(function(e) {
        if (INTERFACE_ENABLED) {
            var regex = new RegExp("^[a-zA-Z0-9 ]+$");
            var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);

            if (e.charCode == 13) {
                //$('#search_form').submit();
                return true;
            }

            if (regex.test(str)) {
                return true;
            }

            e.preventDefault();
            return false;
        }
        else {
            e.preventDefault();
            return false;
        }
    });

    $('body').attr('oncontextmenu', 'return false');
    document.onmousedown=disableClick;
});

/*
Controls the grey-out box. Allows you to turn it on, turn it off, and display a custom message in the box.
*/
/*
function controlGreyOutBox(enable, message) {
    if (message) {
        $('#full-grey-out-message').text(message);
    }

    if (enable) {
        $('#full-grey-out').css('display', 'block');
    }
    else {
        $('#full-grey-out').css('display', 'none');
    }
}
*/

/*
A helper function to enable or disable interaction with the user interface.
If enableInterface is set to true, the interface can be interacted with.
Otherwise, form fields and buttons are disabled, as well as document hit links.
*/
function changeInteractionStatus(enableInterface) {
    var delay_results = parseInt($('#delay_results').val());
    var delay_docview = parseInt($('#delay_docview').val());

    if (enableInterface) {
        INTERFACE_ENABLED = true;
        console.log("Interface to be enabled.");

        // Turn off the progress cursor
        $('*').css('cursor', 'auto');

        // Turn on the search button
        $('#search-button').removeAttr('disabled');
        $('#search-button').attr('value', 'Search');
        $('#search-button').css('background-color', '#EEEEEE');
        $('#search-button').css('color', '#666666');
        $('#search-button').css('cursor', 'pointer');

        // Enable the query field(s)
        $('.searchbox, .smallsearchbox').removeAttr('disabled');

        // Remove the spinner from the first query field
        $('#query').css('background', 'none');

        // Enable the previous/next buttons
        $('.navButton').removeAttr('disabled');
    }
    else {
        INTERFACE_ENABLED = false;
        console.log("Interface to be disabled.");

        // Turn on the progress cursor
        $('*').css('cursor', 'progress');

        // Turn off the search button
        $('#search-button').attr('disabled', 'disabled');
        $('#search-button').attr('value', 'Loading...');
        $('#search-button').css('background-color', '#8B3A3A');
        $('#search-button').css('color', 'white');

        // Add the spinner to the first query field
        $('#query').css('background', 'url(\'/static/images/spinner.gif\')');
        $('#query').css('background-repeat', 'no-repeat');
        $('#query').css('background-position', 'right');

        // Disable the previous/next buttons
        $('.navButton').attr('disabled', 'disabled');
    }

}

/*
Binds anchor clicks with class doc-link with the following code.
Used to enforce "document download" delay times.
*/
function bindDocumentClicks() {
    $('.doc-link').click(
        function(event) {
            event.preventDefault();

            if (INTERFACE_ENABLED) {
                var delay = parseInt($('#delay_docview').val());
                var targetURL = event.target.href;

                if (delay == "") {
                    delay = 0;
                }

                if (delay > 0) {
                    changeInteractionStatus(false);
                    setTimeout(function() {window.location = targetURL;}, (delay * 1000));
                }
                else {
                    window.location = targetURL;
                }
            }
            else {
                alert("We're processing your previous request; please wait.");
            }
    });
}

/*
Bind hovers over search result elements.
Logs the event with an AJAX call for hovering in and a call for hovering out.
*/
function bindResultHovering() {
    $('.search_result').hover(
        function(event) {
            var parent = $(event.target).closest('div[class="search_result"]');
            var trecID = $(parent[0]).attr('id');
            var whooshID = $(parent[0]).attr('whooshid');
            var rank = $(parent[0]).attr('rank');
            var page = $(parent[0]).attr('page');

            $.ajax({
                url: '/treconomics/hover/',
                data: {'status': 'in', 'trecID': trecID, 'whooshID': whooshID, 'rank': rank, 'page': page}
            }).fail(function(data) {
                var responseData = $.parseJSON(data.responseText);

                if ('timeout' in responseData) {
                    alert("Your time for this exercise has expired. We will now redirect you to the next step.");
                    window.location = '/treconomics/next/';
                }
            });
        },
        function(event) {
            var parent = $(event.target).closest('div[class="search_result"]');
            var trecID = $(parent[0]).attr('id');
            var whooshID = $(parent[0]).attr('whooshid');
            var rank = $(parent[0]).attr('rank');
            var page = $(parent[0]).attr('page');

            $.ajax({
                url: '/treconomics/hover/',
                data: {'status': 'out', 'trecID': trecID, 'whooshID': whooshID, 'rank': rank, 'page': page}
            }).fail(function(data) {
                var responseData = $.parseJSON(data.responseText);

                if ('timeout' in responseData) {
                    alert("Your time for this exercise has expired. We will now redirect you to the next step.");
                    window.location = '/treconomics/next/';
                }
            });
    });
}

function bindFormSubmit() {
    $('#search_form').submit(function(event) {
        console.log("Search form submitted.");
        changeInteractionStatus(false);
    });
}

/*
function formSubmit() {
    $("#search_form").submit(function(event) {
        // Only show the waiting box when a delay is enforced
        if (($('#delay_results').val() != "") && (parseInt($('#delay_results').val()) > 0)) {
            controlGreyOutBox(true, "Retrieving results...");
        }

        // If they are present, close all autocomplete boxes upon form submission.

        if ($('.searchbox').hasClass('ui-autocomplete-input')) {
            $('.searchbox').autocomplete('close');
        }

        if ($('.smallsearchbox').hasClass('ui-autocomplete-input')) {
            $('.smallsearchbox').autocomplete('close');
        }

        if ($('#is_fast').val() == 'true') {
            $('#search-button').prop('value', '...');
            $('#search-button').prop('disabled', 'disabled');
        }
    });
}
*/