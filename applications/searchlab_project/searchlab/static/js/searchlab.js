/* maximum number of results per page */
var MAX_PAGE_SIZE = 4


/* global pagination structure */
window.pagination =
{
    results : null,
    pages : 1,
    page : {},
    currentPage : 1
}


/* hide results and pagination containers at page load */
$('#pagination-container').hide();
$('#results-container').hide();


/* override default behaviour of when 'Enter'
 * key pressed. Makes search request instead. */
$('.input').keypress(function(event)
{
   if (event.which == 13)
   {
       event.preventDefault();
       $('#btn-submit').click();
   }
});


/* when search/submit button clicked query terms
 * are stored and a search request is sent */
$('#btn-submit').click(function(event)
{
    event.preventDefault();
    var query_terms = $('#input-search').val();
    searchRequest(query_terms);
});


/* sends an AJAX GET request to Django's search
 * view, paginating results on success.*/
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

/* divides up the result list into pages
 * and returns the first page */
function paginateResults(data)
{
    // store search results
    var results = data["results"];

    // store results in pagination namespace
    window.pagination.results = results;

    // use integer division to determine minimum number of pages
    var pages = ~~(results.length / MAX_PAGE_SIZE);

    // store minimum number of pages in namespace
    window.pagination.pages = pages;

    // if 0 then need at least one page
    if (pages == 0) {
        window.pagination.pages = 1
    }

    // add extra page for remainder results
    if (results.length % MAX_PAGE_SIZE != 0) {
        if (results.length > 5) {
            window.pagination.pages += 1;
        }
    }

    // populate page lookup hash
    var start = 0,
          end = MAX_PAGE_SIZE;

    for (var i=0; i<window.pagination.pages; i++) {
        window.pagination.page[i+1] = results.slice(start, end);
        start += MAX_PAGE_SIZE;
        end += MAX_PAGE_SIZE;
    }

    // display first page
    displayResults(window.pagination.page[1]);
}


/* writes results to the appropriate results
 * div.*/
function displayResults(results)
{
    // set pagination status
    $('#pagination-middle').html(window.pagination.currentPage + " of " + window.pagination.pages);

    clearResults();

    var resultDiv = $('#result-list');

    if (results.length == 0) {

        $('#pagination-container').hide();

        $('<span/>', {
            id: 'no-results',
            text: 'No results found.'
        }).appendTo(resultDiv);
    }

    // cache current page
    var currentPage = window.pagination.currentPage;

    // append results to div, with page derived index
    var index = (currentPage * MAX_PAGE_SIZE) - (MAX_PAGE_SIZE - 1);

    // page derived index attribute assignment
    resultDiv.attr('start', index);

    // add results to div
    for (var i=0; i<results.length; i++) {
        resultDiv.append(createSpannedResult(results[i]));
    }
}

function createSpannedResult(result)
{
    var listElement = $('<li/>');

    // result title
    $('<span/>', {
        class: 'result-title',
        text: result['title']
    }).appendTo(listElement);

    // result description
    $('<span/>', {
        class: 'result-desc',
        text: result['summary']
    }).appendTo(listElement);

    $('<a />', {
        href: result['url'],
        text: result['url']
    }).appendTo(
        $('<span/>', {
            class: 'result-url'
        }).appendTo(listElement));

    return listElement
}


/* clears results from results div. */
function clearResults()
{
    $('#result-list').empty();
    $('#pagination-container').show();
    $('#results-container').show();
}


/* handler for '<<' pagination button */
$('#first').click(function(event)
{
    window.pagination.currentPage = 1;
    displayResults(window.pagination.page[1]);
});

/* handler for '<' pagination button */
$('#previous').click(function(event)
{
    var currentPage = window.pagination.currentPage;
    if (currentPage > 1) {
        currentPage -= 1;
        window.pagination.currentPage = currentPage;
        displayResults(window.pagination.page[currentPage]);
    }
});

/* handler for '<' pagination button */
$('#next').click(function(event)
{
    var currentPage = window.pagination.currentPage;
    if (currentPage < window.pagination.pages) {
        currentPage += 1;
        window.pagination.currentPage = currentPage;
        displayResults(window.pagination.page[currentPage]);
    }
});

/* handler for '<' pagination button */
$('#last').click(function(event)
{
    var final_page = window.pagination.pages;
    window.pagination.currentPage = final_page;
    displayResults(window.pagination.page[final_page]);
});