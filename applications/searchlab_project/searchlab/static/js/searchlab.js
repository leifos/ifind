var MAX_PAGE_SIZE = 13

window.pagination =
{
    results : null,
    pages : null,
    page : {},
    currentPage : 1
}


$('#pagination-container').hide();
$('#results-container').hide();

/* Override default behaviour of when 'Enter'
 * key pressed. Makes search request instead.
 * */
$('.input').keypress(function(event)
{
   if (event.which == 13)
   {
       event.preventDefault();
       $('#btn-submit').click();
   }
});


/* When search/submit button clicked query terms
 * are stored and a search request is sent.
 * */
$('#btn-submit').click(function(event)
{
    event.preventDefault();
    var query_terms = $('#input-search').val();
    searchRequest(query_terms);
});


/* Sends an AJAX GET request to Django's search
 * view, displaying results on success.
 * */
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
    var start = 0;
    var end = MAX_PAGE_SIZE;

    for (var i=0; i<window.pagination.pages; i++) {
        window.pagination.page[i+1] = results.slice(start, end);
        start += MAX_PAGE_SIZE;
        end += MAX_PAGE_SIZE;
    }

    window.pagination.currentPage = 1;

    displayResults(window.pagination.page[1]);
}



/* Writes results to the appropriate results
 * div.
 * */
function displayResults(results)
{
    $('#pagination-middle').html(window.pagination.currentPage + " of " + window.pagination.pages);

    clearResults();

    var resultDiv = $('#result-list');

    if (results.length == 0) {
        $('#pagination-container').hide();
        resultDiv.append("No results found.")
    }

    var currentPage = window.pagination.currentPage;

    if (currentPage == 1) {
        for (var i=0; i<results.length; i++) {
            resultDiv.append(i+1 + " " + results[i]['url'] + '<br />');
        }
    }

    if (currentPage > 1) {
        var index = (currentPage * MAX_PAGE_SIZE) - (MAX_PAGE_SIZE - 1)
        for (var i=0; i<results.length; i++, index++) {
            resultDiv.append(index + " " + results[i]['url'] + '<br />');
        }
    }
}


/* Clears results from results div.
 * */
function clearResults()
{
    $('#result-list').empty();
    $('#pagination-container').show();
    $('#results-container').show();
}


$('#first').click(function(event)
{
    window.pagination.currentPage = 1;
    displayResults(window.pagination.page[1]);
});

$('#previous').click(function(event)
{
    var currentPage = window.pagination.currentPage;
    if (currentPage > 1) {
        currentPage -= 1;
        window.pagination.currentPage = currentPage;
        displayResults(window.pagination.page[currentPage]);
    }
});

$('#next').click(function(event)
{
    var currentPage = window.pagination.currentPage;
    if (currentPage < window.pagination.pages) {
        currentPage += 1;
        window.pagination.currentPage = currentPage;
        displayResults(window.pagination.page[currentPage]);
    }
});

$('#last').click(function(event)
{
    var final_page = window.pagination.pages;
    window.pagination.currentPage = final_page;
    displayResults(window.pagination.page[final_page]);
});