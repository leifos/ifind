var stopHashChange = false;
var interface1Querystring = "";


$(function() {
    // When the search form is submitted...

    $("#search_form").submit(function (event) {
        event.preventDefault();

        $("#progress").css("visibility", "visible");
        $("#whole_page").css("opacity", "0.5");
        $("#whole_page").css("pointerEvents", "none");

        processRequest($("form").serialize());
    });

    $(window).hashchange(function() {
        if (!stopHashChange) {
            doHashSearch();
        }
        stopHashChange = false;
    });

    $(window).hashchange();

});

function processRequest(serializedFormData){
    var query = (serializedFormData.split('query=')[1]);
    var page = serializedFormData.split('&page=')[1];
    var toRemove = ('&page=' + page);
    query = query.replace(toRemove, "");
    if(query!=""){
        if(!page){
            page=1;
        }
        document.location.hash = 'query=' + query  + '&page=' + page;
    }


    console.log(serializedFormData);

    var posting = $.post("ajax_results/", serializedFormData);
    posting.done(function(html){
    var results = $('#ajax_results_div');
    results.empty();
    results.append(html);

    stopHashChange = true;

    $("#progress").css("visibility", "hidden");
    $("#whole_page").css("opacity", "1");
    $("#whole_page").css("pointerEvents", "auto");

    });
}


/*
Checks data supplied as part of the URL hash and performs a search if it is acceptable.
*/
function doHashSearch() {
    var query = getHashValue('query');
    var page = getHashValue('page');


    if (query && query!="") {
        if (!page || isNaN(page)) {
            page = 1;
        }

        if (/\S/.test(query)) {  // Check if string contains at least one non-whitespace character
            var queryField = $('#search_form');
                query = query.replace(/\+/g, ' ');
                queryField.val(query);
                var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

                var formSerialized = "csrfmiddlewaretoken="+ csrf + "&query=" + query + "&page=" + page;

                processRequest(formSerialized);
            }
        }
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

function switchToPage(url) {
    var query = getHashValue('query');
    var page = getHashValue('page');

    var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    var formSerialized = "csrfmiddlewaretoken="+ csrf + "&query=" + query + "&page=" + page;

    processRequest(formSerialized);
}

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