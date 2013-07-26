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
        success: displayResults,
        error: clearResults
    });
}


/* Writes results to the appropriate results
 * div.
 * */
function displayResults(data)
{
    clearResults();

    var resultDiv = $('#result-list');
    var results = data["results"];

    if (results == 0) {
        resultDiv.append("No results found.")
    }

    for (var i=0; i<results.length; i++) {
        resultDiv.append(results[i]['url'] + '<br />');
    }
}


/* Clears results from results div.
 * */
function clearResults()
{
    $('#result-list').empty();
}