/*

Search Helpers for NewsSearch - used for all types of search.

Author: David Maxwell
Date: 2013-11-13
Revision: 1

*/

var INTERFACE_ENABLED = true;

function disableClick(event) {
    if (event.button == 2) {
        return false;
    }
}

$(function() {
    //bindDocumentClicks();
    bindResultHovering();
    bindFormSubmit();

    if ($('#query')) {
        if ($('#focus_querybox').val() == 'true') {
            $('#query').focus();
        }
    }

    $('.searchbox, .smallsearchbox').keypress(function(e) {
        if (INTERFACE_ENABLED) {
            var regex = new RegExp("^[a-zA-Z0-9() \b]+$");
            var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);

            if (e.charCode == 13 || e.keyCode == 13 || e.keyCode == 39 || e.keyCode == 37) {
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
A helper function to enable or disable interaction with the user interface.
If enableInterface is set to true, the interface can be interacted with.
Otherwise, form fields and buttons are disabled, as well as document hit links.
*/
function changeInteractionStatus(enableInterface, useBox) {
    var delay_results = parseInt($('#delay_results').val());
    var delay_docview = parseInt($('#delay_docview').val());

    if (enableInterface) {
        INTERFACE_ENABLED = true;

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
        $('.navButton').css('cursor', 'pointer');

        // Rebind hover events
        bindResultHovering();
    }
    else {
        INTERFACE_ENABLED = false;

        // Turn on the progress cursor
        $('*').css('cursor', 'progress');

        if (useBox) {
            $('#full-grey-out').css('display', 'block');
        }
        else {
            // Turn off the search button
            //$('#search-button').attr('disabled', 'disabled');
            $('#search-button').attr('value', 'Loading...');
            //$('#search-button').css('background-color', '#8B3A3A');
            //$('#search-button').css('color', 'white');

            // Add the spinner to the first query field
            $('#query').css('background', 'url(\'/static/images/spinner.gif\')');
            $('#query').css('background-repeat', 'no-repeat');
            $('#query').css('background-position', 'right');

            // Disable the previous/next buttons
            $('.navButton').attr('disabled', 'disabled');
            //$('.navButton').css('background-color', '#8B3A3A');
            //$('.navButton').css('color', 'white');

            // Remove hover bindings
            $('.search_result').unbind();

            // Hide any autocomplete suggestion boxes
            if ($('.searchbox').hasClass('ui-autocomplete-input')) {
                $('.searchbox').autocomplete('close');
            }

            if ($('.smallsearchbox').hasClass('ui-autocomplete-input')) {
                $('.smallsearchbox').autocomplete('close');
            }

            $('.searchbox, .smallsearchbox').blur();
        }
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
                    changeInteractionStatus(false, true);

                    // Gather information for, and initiate, an AJAX call to indicate that the result is delayed.
                    var parent = $(event.target).closest('div[class="search_result"]');
                    var trecID = $(parent[0]).attr('id');
                    var whooshID = $(parent[0]).attr('whooshid');
                    var rank = $(parent[0]).attr('rank');
                    var page = $(parent[0]).attr('page');

                    $.ajax({
                        url: '/treconomics/docview_delay/',
                        data: {'trecID': trecID, 'whooshID': whooshID, 'rank': rank, 'page': page}
                        }).fail(function(data) {
                            var responseData = $.parseJSON(data.responseText);

                            if ('timeout' in responseData) {
                                alert("Your time for this task has expired. We will now redirect you to the next step.");
                                window.location = '/treconomics/next/';
                            }
                    });

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

//                if ('timeout' in responseData) {
//                    if (!timeoutFlag) {
//                        //alert("Your time for this exercise has expired. We will now redirect you to the next step.");
//                        window.location = APP_ROOT + 'next/';
//                    }
//                    timeoutFlag = true;
//                }
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
//
//                if ('timeout' in responseData) {
//                    if (!timeoutFlag) {
//                        //alert("Your time for this exercise has expired. We will now redirect you to the next step.");
//                        window.location = APP_ROOT + 'next/';
//                    }
//                    timeoutFlag = true;
//                }
            });
    });
}

function bindFormSubmit() {
    $('#search_form').submit(function(event) {
        changeInteractionStatus(false);
    });
}