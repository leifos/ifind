/*

JQuery Autocomplete Query Suggestion Functionality

Author: David Maxwell
Date: 2013-11-07
Revision: 2

*/

$(function() {

    var difference = []; // Stores the difference between an input field before and after a user's change

    /*
    Returns the last word (or partial word) in the input box string.
    This word-in-progress is then sent to the server to provide suggestions as the user types their query.
     */
    function getSuggestion(object, term) {
        var element = $(object[0].element[0]);
        var current = element.val().split(' ');
        var old = element.data('oldVal').split(' ');

        //return (""+term).replace(/[\s-]+$/,'').split(/[\s-]/).pop();
        return getDifferentTerm(old, current);
    }

    /*
    Bind all input fields to have autocomplete functionality.
    Check out http://api.jquery.com/text-selector/ for more information on the selector used.
     */
    $('.searchbox, .smallsearchbox').autocomplete({
        minLength: 1,
        source: function(request, response) {
            var selectedElement = $(this.element);
            var currFieldValue = selectedElement[0].value;
            var previousValue = selectedElement.data('oldVal');

            oldArray = previousValue.split(' ');
            newArray = currFieldValue.split(' ');

            difference = getDifferentTerm(oldArray, newArray);

            function getSuggestionString(difference, selectedItem, element, fieldValue, rank) {
                var suggestionValue = '<p class="autocomplete-item" rank="' + rank + '">';

                if (previousValue === undefined || previousValue == "") {
                    suggestionValue += "<strong>" + selectedItem + "</strong>";
                }
                else {
                    for (termIndex in newArray) {
                        if (termIndex == difference[1]) {
                            if (termIndex == 0) suggestionValue += "<strong>" + selectedItem + "</strong>";
                            else suggestionValue += " <strong>" + selectedItem + "</strong>";
                        }
                        else {
                            if (termIndex == 0) suggestionValue += newArray[termIndex];
                            else suggestionValue += " " + newArray[termIndex];
                        }
                    }
                }

                element.data('oldVal', fieldValue);
                return suggestionValue + '</p>';
            }

            function getSuggestionRank(results, suggestion) {
                for (var i in results) {
                    i = parseInt(i);

                    if (results[i] == suggestion)
                        return i + 1;
                }

                return -1;
            }

            var affectedWord = getSuggestion($(this), request.term)[0];

            if (typeof(affectedWord) !== 'undefined' && affectedWord != "") {
                $.ajax({
                    url: APP_ROOT + 'autocomplete/',
                    dataType: "json",
                    data: {
                        suggest: affectedWord
                    },
                    success: function(data) {
                        response( $.map( data.results, function(item) {
                            var rank = getSuggestionRank(data.results, item);
                            return {
                                label: getSuggestionString(difference, item, selectedElement, currFieldValue, rank),
                                value: item}
                            }));
                    },
                    error: function(data) {
                        // If there was an error, we tell the user.
                        if ('error' in data) {
                            alert("Something went wrong with your request!");
                        }

                        // If the experiment's time has been reached, we alert the user and redirect.
                        if ('timeout' in data) {
                            alert("Your time for this exercise has expired.");
                            window.location = APP_ROOT + 'next/';
                        }
                    }});
            }
        },
        //autoFocus: true, // Focus on the first element by default
        focus: function(event, ui) {
            event.preventDefault();

            var label_element = $(ui.item.label);
            var suggestion = ui.item.value;
            var rank = label_element.attr('rank');

            $.ajax({
                url: '/treconomics/suggestion_hover/',
                data: {'suggestion': suggestion, 'rank': rank}
            });
        },
        select: function(event, ui) {
            event.preventDefault();
            var currFieldValue = event.target.value;
            var previousValue = $(this).data('oldVal');

            var selectedItem = ui.item.value;
            var newFieldValue = "";

            oldArray = previousValue.split(' ');
            newArray = currFieldValue.split(' ');

            if (previousValue === undefined || previousValue == "") {
                newFieldValue = selectedItem
            }
            else {
                for (termIndex in newArray) {
                    if (termIndex == difference[1]) {
                        if (termIndex == 0) newFieldValue += selectedItem;
                        else newFieldValue += " " + selectedItem;
                    }
                    else {
                        if (termIndex == 0) newFieldValue += newArray[termIndex];
                        else newFieldValue += " " + newArray[termIndex];
                    }
                }
            }

            event.target.value = newFieldValue;

            // Log the event - the user has selected a new word, query is now...
            $.ajax({
                url: APP_ROOT + 'suggestion_selected/',
                data: {'added_term': selectedItem, 'new_query': newFieldValue}
            });
      }
    });

    // For each query box, update the _renderItem function for autocomplete. This ensures HTML is rendered correctly. */
    $.each($('.searchbox, .smallsearchbox'), function(index, item) {
        $(item).data('ui-autocomplete')._renderItem = function(ul, item) {
            return $("<li></li>")
             .data("item.autocomplete", item)
             .append("<a>" + item.label + "</a>")
             .appendTo(ul);
        };
    });

    // When the page loads, set each input text field to have an oldVal property.
    $(document).ready(function() {
        $(':text').each(function(i, obj) {
            var element = $(obj);
            element.data('oldVal', element.val());
        });
    });
});

/*
A function which returns the term that appears within two arrays differently.
This is used to determine which word to focus on in the suggestion box.
An array is returned, containing the differing term at [0] and the position of the word (zero-based) at [1].
*/
function getDifferentTerm(oldArray, newArray) {
    var returnArray = [];
    var i = 0;

    jQuery.grep(newArray, function(element) {
        if (jQuery.inArray(element, oldArray) == -1) {
            returnArray = [element, i];
        }

        i++;
    });

    return returnArray;
}