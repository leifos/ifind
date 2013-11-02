/*

JQuery AJAX Search Functionality

Author: David Maxwell
Date: 2013-10-31
Revision: 1

*/

function switchToPage(url) {
    alert(url);
}

$(function() {

    /*
    Returns the last word (or partial word) in the input box string.
    This word-in-progress is then sent to the server to provide suggestions as the user types their query.
     */
    function getSuggestion(term) {
        return (""+term).replace(/[\s-]+$/,'').split(/[\s-]/).pop();
    }

    /*
    Removes the last (presumably incomplete) word from the given string and returns the spliced string.
    From this shortened string, we can then add our complete suggestion to the query string.
     */
    function removeSuggestionText(inputString) {
        var lastSpaceIndex = inputString.lastIndexOf(" ");
        return inputString.substring(0, lastSpaceIndex);
    }

    /*
    Bind all input fields to have autocomplete functionality.
    Check out http://api.jquery.com/text-selector/ for more information on the selector used.
     */
    $(":text").autocomplete({
      minLength: 2,
      source: function( request, response ) {

        $.ajax({
          url: "",
          dataType: "json",
          data: {
            suggest: getSuggestion(request.term)
          },
          success: function( data ) {
            response( $.map( data.results, function( item ) {
              return {
                label: item,
                value: item
              }
            }));
          }
        });
      },
      select: function(event, ui) {
          event.preventDefault();
          var previousValue = $(this).attr('previousSuggestion');
          var currFieldValue = event.target.value;
          var selectedItem = ui.item.value;
          var newFieldValue;

          if (previousValue === undefined) {
              newFieldValue = selectedItem
          }
          else {
              newFieldValue =  removeSuggestionText(currFieldValue) + " " + selectedItem;
          }

          event.target.value = newFieldValue;
          $(this).attr('previousSuggestion', newFieldValue);
      }

    });

    $("#search_form").submit(function(event) {
        event.preventDefault();
        var posting = $.post("", $("form").serialize());

        posting.done(function(data) {
            var results = $('div.results');
            results.empty(); // Remove all children for the new results set

            // Add the top part
            results.append('<div class="query"><strong>Search Terms: <em>' + data['query'] + '</em></strong> <span>Showing page <em>' + data['curr_page'] + '</em> out of <em>' + data['num_pages'] + '</em> pages.</span></div>');

            // Add each of the results
            for (var result_no in data['trec_results']) {
                var result = data['trec_results'][result_no];
                results.append('<div class="entry" id="' + result['docid'] + '"><p class="result_title"><a href="' + result['url'] + '"><strong>' + result['title'] + '</strong></a></p><p class="summary">' + result['summary'] + '</p></div>');
                results.append('<div class="byline">' + result['source'] + '</div>');
            }

            console.log(data);

            // Add navigation buttons at bottom of page (if applicable)
            var results_nav = $('div.results_nav');
            results_nav.empty();

            var nextButton = "";
            var prevButton = "";

            if (data['curr_page'] < data['num_pages']) {
                nextButton = '<input class="largebutton" type="button" onclick="switchToPage(\'' + data['next_page_link'] + '\');" value="Next Page" />';
            }

            if (data['curr_page'] > 1) {
                prevButton = '<input class="largebutton" type="button" onclick="switchToPage(\'' + data['prev_page_link'] + '\');" value="Prev Page" />';
            }

            results_nav.append('<div class="result_nav"><center><form>' + prevButton + nextButton + '</form></center></div>');



            /*<center>
              <form>
                <input class="largebutton" type="button" onclick=
                "parent.location='?query=test&amp;page=2'" value="Next Page" />
                <!-- a href="?query=test&amp;page=2">Next Page</a -->
              </form>
            </center>*/
        });

    });

  });