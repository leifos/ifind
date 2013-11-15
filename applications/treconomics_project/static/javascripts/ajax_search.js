/*

JQuery AJAX Search Functionality

Author: David Maxwell
Date: 2013-11-03
Revision: 2

*/

var stopHashChange = false;
var interface1Querystring = "";

$(function() {
    // When the search form is submitted...
    $("#search_form").submit(function(event) {
        event.preventDefault();
        processRequest($("form").serialize());
        interface1Querystring = "";
    });

    // When the URL hash changes, check the data and see if a search can be performed.
    $(window).hashchange(function() {
        if (!stopHashChange)
            doHashSearch();

        stopHashChange = false;
    });

    $(window).hashchange();
});

/*
Switches the current search results to the page specified by the URL supplied.
*/
function switchToPage(url) {
    var page_interface = $('#interface_type');

    if (parseInt(page_interface.val()) == 1) {
        var pageNumber = getPageNumber(url);

        if (interface1Querystring != "") {
            interface1Querystring += '&page=' + pageNumber;
            processRequest(interface1Querystring, true);
        }
        else {
            var pageNumber = getPageNumber(url);
            var formData = $("form").serialize();
            formData = formData + '&page=' + pageNumber;

            processRequest(formData, true);
        }
    }
    else {
        var pageNumber = getPageNumber(url);
        var formData = $("form").serialize();
        formData = formData + '&page=' + pageNumber;

        processRequest(formData, true);
    }
}

/*
Returns the page number that has been requested from the given URL.
*/
function getPageNumber(url) {
    if (url.substring(0, 1) == '?') {
        url = url.substring(1, url.length);
    }

    var vars = url.split('&');

    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');

        if (pair[0] == 'page') {
            return parseInt(pair[1]);
        }
    }

    return false;
}

/*
The URL hash (everything after the #, including the #) is being used in a querystring-style format.
Specify a key as the parameter for this function and you'll get the corresponding value.
With a hash of #query=bbc&page=2, getHashValue('query') returns 'bbc'.

Solution adapted from http://stackoverflow.com/a/3788235.
*/
function getHashValue(key) {
    var re = new RegExp('(?:\\#|&)'+key+'=(.*?)(?=&|$)','gi');
    var r = [];
    var m;

    while ((m = re.exec(document.location.hash)) != null) {
        r.push(m[1]);
    }

    if(typeof(r[0]) === 'undefined') {
        return false;
    }

    return r[0];
}

/*
Function which processes the AJAX request. Sends the request and displays the results on the page.
*/
function processRequest(serializedFormData, noDelay) {
    $('*').css('cursor', 'progress');

    if (noDelay) {
        serializedFormData += '&noDelay=true';
    }

    var posting = $.post("", serializedFormData);

    posting.fail(function(data) {
        $('body').css('cursor', 'default');
        alert("Something went wrong when processing your request!");
        console.log("Server error on AJAX request: " + data.responseText);
    });

    posting.done(function(data) {
        var results = $('div.results');
        results.empty(); // Remove all children for the new results set

        var results_nav = $('div.results_nav');
        results_nav.empty(); // Remove all children from the navigation button container

        if ('timeout' in data) {
            results.append('<div class="query" style="text-align: center;"><strong>Task Timed Out.</strong><br />Your search task has timed out. Please click <a href="/treconomics/next/">here</a> to continue.</div>');
        }
        else {
            if (data['trec_search']) {
                // Add the top part
                results.append('<div class="query"><strong>Search Terms: <em>' + data['query'] + '</em></strong> <span>Showing page <em>' + data['curr_page'] + '</em> out of <em>' + data['num_pages'] + '</em> page(s).</span></div>');

                // Add each of the results
                for (var result_no in data['trec_results']) {
                    var result = data['trec_results'][result_no];
                    results.append('<div class="search_result" id="' + result['docid'] + '" rank="' + result['rank'] + '" page="' + data['curr_page'] + '" whooshid="' + result['whooshid'] + '"><div class="entry"><p class="result_title"><strong><a href="' + result['url'] + '">' + result['title'] + '</a></strong></p><p class="summary">' + result['summary'] + '</p></div><div class="byline">' + result['source'] + '</div></div>');
                }

                // Add navigation buttons at bottom of page (if applicable)
                var nextButton = "";
                var prevButton = "";

                if (data['curr_page'] < data['num_pages']) {
                    nextButton = '<input class="navButton largebutton" type="button" onclick="switchToPage(\'' + data['next_page_link'] + '\');" value="Next Page" />';
                }

                if (data['curr_page'] > 1) {
                    prevButton = '<input class="navButton largebutton" type="button" onclick="switchToPage(\'' + data['prev_page_link'] + '\');" value="Prev Page" />';
                }

                results_nav.append('<div class="result_nav"><center><form>' + prevButton + nextButton + '</form></center></div>');
            }
            else {
                results.append('<div class="query"><strong>Search Terms: <em>' + data['query'] + '</em></strong> <span>No results found.</span></div>');
            }

            stopHashChange = true;

            if ('curr_page' in data) {
                window.location.hash = 'query=' + data['query'] + '&page=' + data['curr_page'];
            }
            else {
                window.location.hash = 'query=' + data['query'];
            }
        }

        bindResultHovering(); // Bind hovering actions to the new document elements.
        $('*').css('cursor', 'default');
        $('a').css('cursor', 'pointer');
        $('.navButton').css('cursor', 'pointer');
        $('body').scrollTop(0);
    });
}

/*
Checks data supplied as part of the URL hash and performs a search if it is acceptable.
*/
function doHashSearch() {
    var page_interface = $('#interface_type');
    var query = getHashValue('query');
    var page = getHashValue('page');

    if (query) {
        if (!page || isNaN(page)) {
            page = 1;
        }

        if (/\S/.test(query)) {  // Check if string contains at least one non-whitespace character
            var queryField = $('#query');

            if (parseInt(page_interface.val()) != 1) {
                query = query.replace(/\+/g, ' ');
                queryField.val(query);
                var formSerialized = $('form').serialize();
                formSerialized += '&page=' + page;
                processRequest(formSerialized, true);
            }
            else {
                // With an interface of 1, we have to pull the previous querystring from the server!
                $.ajax({
                    url: APP_ROOT + 'ajax_search_querystring/',
                    success: function(data) {
                        interface1Querystring = data['querystring'];
                        interface1Querystring += '&page=' + page;
                        interface1Querystring += '&noDelay=true';
                        interface1Querystring += '&csrfmiddlewaretoken=' + $('input[name=csrfmiddlewaretoken]').val();
                        processRequest(interface1Querystring, true);
                    }
                });
            }
        }
    }
}