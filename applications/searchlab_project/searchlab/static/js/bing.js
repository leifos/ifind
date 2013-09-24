////////////////////////////////
// String formatting function //
////////////////////////////////

String.prototype.format = function()
{
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number)
  {
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};

////////////////////////////////
// String capitalise function //
////////////////////////////////

String.prototype.capitalise = function()
{
    return this.charAt(0).toUpperCase() + this.slice(1);
}

//////////////////////////////
// JQuery element existence //
//////////////////////////////

jQuery.fn.exists = function()
{
    return this.length>0;
}

////////////////////////
// Pagination Globals //
////////////////////////

window.pagination =
{
    maxPageSize: 9,             // max results per page
    results : null,             // list of results
    pages : 1,                  // how many pages there are
    page : {},                  // page lookup map
    currentPage : 1             // current page
};

////////////////////////
//   Search Globals   //
////////////////////////

window.search =
{
    result_type :'image'
};

/////////////////////////////
// Cached JQuery Selectors //
/////////////////////////////

var paginationContainer = $('#pagination-container');
var resultsContainer = $('#results-container');
var dropdownOptions = $('#dropdown-options');
var searchInput = $('#search-input');

/////////////////////////////
//          MAIN?          //
/////////////////////////////

// hide pagination, results and focus search input
paginationContainer.hide();
resultsContainer.hide();
searchInput.focus();

// hide option that's search default and set the button to it
$('#dropdown-options > li > a[href="{0}"]'.format(window.search.result_type)).css('display', 'none');
$('#submit-btn').text('{0} Search'.format(window.search.result_type.capitalise()));

// when page ready (has loaded?)
$(document).ready(function()
{
    // handle submit button dropdown options
    $('#dropdown-options > li').click(function(e) {
        e.preventDefault();
        var selectedType = e.target.getAttribute("href");
        $('#dropdown-options > li > a').filter(':hidden').show();
        $('#dropdown-options > li > a[href="{0}"]'.format(selectedType)).css('display', 'none');
        window.search.result_type = selectedType;
        $('#submit-btn').text('{0} Search'.format(e.target.textContent));
        $('#dropdown-container').hide();
        console.log(window.search.result_type);
    });

    // detect key down event
    $(document).keydown(function(event)
    {
        // <ENTER> key submits search
        if (event.which == 13)
        {
           event.preventDefault();
           $('#submit-btn').click();
        }

        // if searchInput not in use, use arrow keys for pagination
        if (!$('*:focus').is(searchInput))
        {
            // right arrow
            if (event.which == 39)
            {
                event.preventDefault();
                $('#next-btn').click();
            }

            // left arrow
            if (event.which == 37)
            {
                event.preventDefault();
                $('#previous-btn').click();
            }
        }
    });

    // detects when submit button clicked and fires a request
    $('#submit-btn').click(function(event)
    {
        event.preventDefault();
        searchRequest(searchInput.val());
    });


    /* handler for '<<' pagination button */
    $('#first-btn').click(function(event)
    {
        window.pagination.currentPage = 1;
        displayResults(window.pagination.page[1]);
    });

    /* handler for '<' pagination button */
    $('#previous-btn').click(function(event)
    {
        var currentPage = window.pagination.currentPage;
        if (currentPage > 1) {
            currentPage -= 1;
            window.pagination.currentPage = currentPage;
            displayResults(window.pagination.page[currentPage]);
        }
    });

    /* handler for '>' pagination button */
    $('#next-btn').click(function(event)
    {
        var currentPage = window.pagination.currentPage;
        if (currentPage < window.pagination.pages) {
            currentPage += 1;
            window.pagination.currentPage = currentPage;
            displayResults(window.pagination.page[currentPage]);
        }
    });

    /* handler for '<' pagination button */
    $('#last-btn').click(function(event)
    {
        var final_page = window.pagination.pages;
        window.pagination.currentPage = final_page;
        displayResults(window.pagination.page[final_page]);
    });
});

// sends an AJAX GET request to searchlab, paginating results on success
function searchRequest(query_terms)
{
    $.ajax
    ({
        type: "GET",
        url: "/search/",
        data: {'q' : query_terms,
               't' : window.search.result_type},
        success: paginateResults
    });
}

// calculates and initialises pagination, passing first page to be displayed
function paginateResults(data)
{
    // store search results
    var results = data["results"];
    window.pagination.results = results;

    var maxPageSize = window.pagination.maxPageSize;

    // store minimum number of pages in namespace
    var pages = ~~(results.length / maxPageSize);
    window.pagination.pages = pages;

    // if 0 then need at least one page
    if (pages == 0)
    {
        window.pagination.pages = 1
    }

    // add extra page for remainder results
    if (results.length % maxPageSize != 0) {
        if (results.length > 5)
        {
            window.pagination.pages += 1;
        }
    }

    // populate page lookup hash
    var start = 0,
          end = maxPageSize;

    for (var i=0; i<window.pagination.pages; i++)
    {
        window.pagination.page[i+1] = results.slice(start, end);
        start += maxPageSize;
        end += maxPageSize;
    }

    // display first page
    displayResults(window.pagination.page[1]);
}

// displays single page
function displayResults(results)
{
    // clear previous results
    resultsContainer.hide().empty();
    paginationContainer.hide();

    // set pagination status
    $('#page-btn').html(window.pagination.currentPage + " of " + window.pagination.pages);

    // if no results
    if (results.length == 0) {
        $('<span/>', {
            id: 'no-results',
            text: 'No results found.'
        }).appendTo(resultsContainer);
    }

    else
    {
        // cache current page
        var currentPage = window.pagination.currentPage;
        var maxPageSize = window.pagination.maxPageSize;

        // append results to div, with page derived index
        var index = (currentPage * maxPageSize) - (maxPageSize - 1);

        // page derived index attribute assignment
        resultsContainer.attr('start', index);

        if (window.search.result_type == 'image')
        {
            var resultHTML = $('#image-result-template').html();

            for (var i=0; i<results.length; i++)
            {
                var fileSize = results[i]['file_size'];
                var dimensions = "{0} x {1}".format(results[i]['width'], results[i]['height']);
                var mediaUrl = results[i]['media_url'];
                var thumbURL = results[i]['thumb_url'];

                var overlayString = "{0}Kb<br>{1}".format(fileSize, dimensions);

                resultsContainer.append(resultHTML.format(mediaUrl, thumbURL, overlayString));
            }
        }
        else if (window.search.result_type == 'video')
        {
            var resultHTML = $('#video-result-template').html();

            for (var i=0; i<results.length; i++)
            {
                var mediaUrl = results[i]['media_url'];
                var runTime = results[i]['run_time'];
                var title = results[i]['title'];
                var thumbUrl = results[i]['thumb_url'];

                var overlayString = "{0}<br>{1}".format(title, runTime);

                resultsContainer.append(resultHTML.format(mediaUrl, thumbUrl, overlayString));
            }
        }
        else if (window.search.result_type == 'web')
        {
            var resultHTML = $('#web-result-template').html();

            for (var i=0; i<results.length; i++)
            {

                var title = results[i]['title'];
                var summary = results[i]['summary'];
                var url = results[i]['url'];

                resultsContainer.append(resultHTML.format(url, title, url, summary));
            }
        }
    }

    paginationContainer.fadeIn("slow");
    resultsContainer.fadeIn("fast");
    searchInput.blur();
}
