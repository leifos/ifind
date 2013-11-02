/*

JQuery AJAX Search Functionality

Author: David Maxwell
Date: 2013-10-31
Revision: 1

*/

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
    $( ":text" ).autocomplete({
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

  });