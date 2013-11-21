/*

Search Helpers for NewsSearch - used for all types of search.

Author: David Maxwell
Date: 2013-11-13
Revision: 1

*/

$(function() {
    bindResultHovering();
    formSubmit();

    if ($('#query')) {
        $('#query').focus();
    }
});

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
        });
    });
}

function formSubmit() {
    $("#search_form").submit(function(event) {
        // Only show the waiting box when a delay is enforced
        if (($('#delay_results').val() !== 'undefined') || (parseInt($('#delay_results').val()) > 0)) {
            $('#full-grey-out').css('display', 'block');
        }

        // If they are present, close all autocomplete boxes upon form submission.

        if ($('.searchbox').hasClass('ui-autocomplete-input')) {
            $('.searchbox').autocomplete('close');
        }

        if ($('.smallsearchbox').hasClass('ui-autocomplete-input')) {
            $('.smallsearchbox').autocomplete('close');
        }
    });
}