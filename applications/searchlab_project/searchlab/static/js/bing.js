////////////////////////////////
// String formatting function //
////////////////////////////////

String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) {
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};

////////////////////////
// Pagination Globals //
////////////////////////

// global pagination vars
window.pagination =
{
    maxPageSize: 4,             // max results per page
    results : null,             // list of results
    pages : 1,                  // how many pages there are
    page : {},                  // page lookup map
    currentPage : 1             // current page
};

///////////////////
// Cached JQuery //
///////////////////

var paginationContainer = $('#pagination-container');
var resultsContainer = $('#results-container');
var searchInput = $('#search-input');


// hide pagination, results and focus search input
paginationContainer.hide();
resultsContainer.hide();
searchInput.focus();

// override LEFT and RIGHT arrow keys and map to pagination buttons
$(document).keydown(function(event)
{

    if (event.which == 13)
    {
       event.preventDefault();
       $('#submit-btn').click();
    }


    if (!$('*:focus').is(searchInput)) {

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

// query terms stored and a search request is sent
$('#submit-btn').click(function(event)
{
    event.preventDefault();
    var query_terms = searchInput.val();
    searchRequest(query_terms);
});


// sends an AJAX GET request to searchlab, paginating results on success
function searchRequest(query_terms)
{
    $.ajax
    ({
        type: "GET",
        url: "/search/",
        data: {'q' : query_terms},
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
    if (pages == 0) {
        window.pagination.pages = 1
    }

    // add extra page for remainder results
    if (results.length % maxPageSize != 0) {
        if (results.length > 5) {
            window.pagination.pages += 1;
        }
    }

    // populate page lookup hash
    var start = 0,
          end = maxPageSize;

    for (var i=0; i<window.pagination.pages; i++) {
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

    else {
        // cache current page
        var currentPage = window.pagination.currentPage;
        var maxPageSize = window.pagination.maxPageSize;

        // append results to div, with page derived index
        var index = (currentPage * maxPageSize) - (maxPageSize - 1);

        // page derived index attribute assignment
        resultsContainer.attr('start', index);

        var resultHTML = $('#result-template').html();

        // add results to div
        for (var i=0; i<results.length; i++) {

            var title = results[i]['title'];
            var summary = results[i]['summary'];
            var url = results[i]['url'];

            resultsContainer.append(resultHTML.format(url, title, url, summary));
        }
        paginationContainer.fadeIn("slow");
    }

    resultsContainer.fadeIn("fast");
    searchInput.blur();
}


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
