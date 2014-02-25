var button_available = true;

$(function () {
    initiate_game();
    var timeoutID;
    //window.onbeforeunload = confirmExit;
    //function confirmExit()
    //{
    //    return 'Are you sure you want to quit the game?';
    //}

    var skip_options = {
        trigger: 'hover',
        content: 'Move on to the next page',
        placement: 'bottom',
        delay: { show: 100, hide: 100 }
    }
    $('#skip-button').popover(skip_options)
    var skip_options = {
        trigger: 'hover',
        content: 'send the query to the search engine',
        placement: 'bottom',
        delay: { show: 100, hide: 100 }
    }
    $('#search-button').popover(skip_options)

    $(window).resize(function () {
        var search_div_width = $('#search-div').width();
        $('#query').width(search_div_width - 20);
    });

    $(document).keypress(function (event) {
        if (event.ctrlKey && event.which == 13) {
            skip_button_click(event);
        }
        else if (event.which == 13) {
            search_button_click(event);
        }
    });

    $('#search-button').click(function (event) {
        search_button_click(event);
    });

    $('#skip-button').click(function (event) {
        skip_button_click(event);
    });
});

function search_success(data, textStatus, jqXHR) {
    $('body').css({'cursor': 'auto'});
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1) {
        window.location = "/pagefetch/game_over";
        window.onbeforeunload = null;
        return false;
    }
    var obj_list = jQuery.parseJSON(obj.results);
    var html_string = "";
    $(obj_list).each(function () {
            if (this.link != obj.url_to_find) {
                html_string += "<Li><strong>" + this.title + "</strong></Li>";
            }
            else {
                html_string += "<Li class='text-warning'><strong>" + "Page was retrieved in this rank" + "</strong></Li>";
            }
        }
    );
    $('#search-results-ol').html(html_string);

    var game_updates_html = "<tr><td><h4> current score :</h4></td><td><h4>" + obj.current_score + "</h4></td></tr>" +
        "<tr><td><h4> round no :</h4></td><td><h4>" + obj.no_round + "</h4></td></tr>" +
        //"<tr><td><h4>remaining rounds :</h4></td><td><h4>"+ obj.no_remaining_rounds +"</h4></td></tr>"+
        "<tr><td><h4>queries issued for this page :</h4></td><td><h4>" + obj.no_of_queries_issued_for_current_page + "</h4></td></tr>";
    $('#game_updates-div').html(game_updates_html);
    //$('#score-div').html("<h1 class='text-center'>" + obj.score +"</h1>");
    $('#score-div').html("<p class='lead text-center'><strong>" + obj.score + "/1000<strong></p>");
    $('#avatar-div').html("<h3>" + obj.avatar + "</h3>")
    if (obj.score != 0) {
        $('#skip-button').html("<i class='icon-forward icon-white'></i> take points");
        $('#skip-button').removeClass("btn-error").addClass("btn-success");
        $('#search-button').html('<i class="icon-search icon-white"></i> search again');
        $('#content-div').removeClass("alert-error").addClass("alert-success");
    }
    else {
        $('#skip-button').html("<i class='icon-forward icon-white'></i> skip");
        $('#skip-button').removeClass("btn-success").addClass("btn-danger");
        $('#search-button').html('<i class="icon-search icon-white"></i> search again');
        $('#content-div').removeClass("alert-success").addClass("alert-error");
    }
    adjust_body_divs_height();
    button_available = true;
    $('#search-button').removeAttr("disabled");
}
function get_score(data, textStatus, jqXHR) {
    var obj = jQuery.parseJSON(data);
    return obj.current_score;
}

function display_next_page_success(data, textStatus, jqXHR) {
    $('#query').val("");
    $('#query').focus();
    $('#content-div').removeClass("alert-success");
    $('#content-div').addClass("alert-error");
    $('#skip-button').removeClass("btn-success").addClass("btn-danger");

    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1) {
        window.onbeforeunload = null;
        window.location = "/pagefetch/game_over";
        return false;
    }
    var game_updates_html = "<tr><td><h4> current score :</h4></td><td><h4>" + obj.current_score + "</h4></td></tr>" +
        "<tr><td><h4> round no :</h4></td><td><h4>" + obj.no_round + "</h4></td></tr>" +
        //"<tr><td><h4>remaining rounds :</h4></td><td><h4>"+ obj.no_remaining_rounds +"</h4></td></tr>"+
        "<tr><td><h4>queries issued for this page :</h4></td><td><h4>" + obj.no_of_queries_issued_for_current_page + "</h4></td></tr>";

    $("#counter").flipCounter(
        "startAnimation", // scroll counter from the current number to the specified number
        {
            //number: 0,
            end_number: obj.current_score, // the number we want the counter to scroll to
            easing: jQuery.easing.easeOutCubic, // this easing function to apply to the scroll.
            duration: 1000, // number of ms animation should take to complete
        }
    );

    $('#game_updates-div').html(game_updates_html);
    $('#search-results-ol').html("");
    $('#score-div').html("");
    $('#avatar-div').html("<h3>" + obj.avatar + "</h3>")
    $('#skip-button').html("<i class='icon-forward icon-white'></i> skip");
    $('#search-button').html('<i class="icon-search icon-white"></i> search');
    $('#image-box').hide();
    $('#image-div').html("<image src= '" + obj.screenshot + "' style='background-color:white;' height='1000' width='1000'> </image>");
    adjust_body_divs_height();
}

function adjust_header_divs_height() {
    var highestCol = Math.max($('#statistics-div').height(), $('#header-div').height());
    $('#statistics-div').height(highestCol);
    $('#header-div').height(highestCol);
}

function adjust_body_divs_height() {
    var search_div_height = $('#search-div').height();
    var content_div_height = $('#content-div').height();
    var search_div_margin = $('#search-div').css("margin-bottom");
    var variable = search_div_height + content_div_height;
    var highestCol = Math.max($('#image-div').height(), variable);
    if (highestCol < 770) {
        highestCol = 770;
    }
    $('#image-div').height(highestCol);
    $('#content-div').height(highestCol - search_div_height - 35);
}

function adjust_search_input_width() {
    var search_div_width = $('#search-div').width();
    $('#query').width(search_div_width - 20);
}

function avatar() {
    $('#search-div').fadeTo(0, 0);
    $('#content-div').fadeTo(0, 0);
    $('#image-div').fadeTo(0, 0);
    $('#avatar-div').html("<h3> Ready? </h3>")
    timeoutID = window.setTimeout(avatar1, 2000);
}

function avatar1() {
    timeoutID = window.setTimeout(avatar1, 2000);
    $('#search-div').fadeTo(1500, 1);
    $('#content-div').fadeTo(1500, 1);
    $('#image-div').fadeTo(1500, 1);
    $('#avatar-div').html("<h3> Fetch the page to score points!  </h3>")
    window.clearTimeout(timeoutID);
}

function initiate_game() {
    var game_updates_html = "<tr><td><h4> score :</h4></td><td><h4> 0 </h4></td></tr>" +
        "<tr><td><h4> round no :</h4></td><td><h4> 1 </h4></td></tr>" +
        //"<tr><td><h4> remaining rounds :</h4></td><td><h4> 4 </h4></td></tr>"+
        "<tr><td><h4> queries issued for this page :</h4></td><td><h4> 0 </h4></td></tr>";
    $('#game_updates-div').html(game_updates_html);
    avatar();
    adjust_header_divs_height();
    adjust_body_divs_height();
    adjust_search_input_width();
}

function search_button_click(event) {
    var opts = {
        lines: 6, // The number of lines to draw
        length: 4, // The length of each line
        width: 4, // The line thickness
        radius: 3, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        rotate: 0, // The rotation offset
        direction: 1, // 1: clockwise, -1: counterclockwise
        color: '#000', // #rgb or #rrggbb
        speed: 1, // Rounds per second
        trail: 60, // Afterglow percentage
        shadow: false, // Whether to render a shadow
        hwaccel: false, // Whether to use hardware acceleration
        className: 'spinner', // The CSS class to assign to the spinner
        zIndex: 2e9, // The z-index (defaults to 2000000000)
        top: 'auto', // Top position relative to parent in px
        left: 'auto' // Left position relative to parent in px
    };
    var target = document.getElementById('score-div');
    var spinner = new Spinner(opts).spin(target);
    if (button_available == true) {
        event.preventDefault();
        button_available = false;
        $('#search-button').attr("disabled", "disabled");
        $(this).css({'cursor': 'wait'});
        $.ajaxSetup({
            // Disable caching of AJAX responses
            cache: false});
        $.ajax
        ({
            cache: false,
            type: "GET",
            url: "/pagefetch/search/",
            data: {
                'query': $('#query').val()
            },
            success: search_success,
            error: function (xhr, ajaxOptions) {
                $('#score-div').html("<Strong>Error occured</strong>");
                noty({text: xhr.status + " : " + xhr.responseText, type: 'error'});
                onComplete(error);
            },
            dataType: 'html'
        });
    }
}

function skip_button_click(event) {
    event.preventDefault();
    $.ajaxSetup({
        // Disable caching of AJAX responses
        cache: false});
    $.ajax
    ({
        cache: false,
        type: "GET",
        url: "/pagefetch/display_next_page/",
        success: display_next_page_success,
        dataType: 'html'
    });
}
