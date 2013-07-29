$(function()
{
    initiate_game();
    var timeoutID;
    window.onbeforeunload = confirmExit;
    function confirmExit()
    {
        return 'Are you sure you want to quit the game?';
    }
    $(window).resize(function()
     {
        var search_div_width =$('#search-div').width();
        $('#query').width(search_div_width -20);
     });

    $(document).keypress(function(event)
    {
        if(event.ctrlKey && event.which == 13)
        {
            $(this).css({'cursor':'wait'});
            event.preventDefault();
            $.ajax
            ({
                type: "GET",
                url: "/rmiyc/display_next_page/",
                success: display_next_page_success,
                dataType: 'html'
            });
        }
        else if(event.which == 13)
        {
             event.preventDefault();
            $.ajax
            ({
                type: "GET",
                url: "/rmiyc/search/",
                data:
                {
                    'query' : $('#query').val()
                },
                success: search_success,
                dataType: 'html'
            });
        }
    });

    $('#search-button').click(function(event)
    {
        event.preventDefault();
        //$('#search-button').attr("disabled", true);
        $('body').css({'cursor':'wait'});
        $.ajax
        ({
            type: "GET",
            url: "/rmiyc/search/",
            data:
            {
                'query' : $('#query').val()
            },
            success: search_success,
            dataType: 'html'
        });

    });

    $('#skip-button').click(function(event)
    {
        event.preventDefault();
        $.ajax
        ({
            type: "GET",
            url: "/rmiyc/display_next_page/",
            success: display_next_page_success,
            dataType: 'html'
        });
    });
});

function search_success(data, textStatus, jqXHR)
{
    //$('#search-button').removeAttr("disabled");
    $('body').css({'cursor':'auto'});
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.location ="/rmiyc/game_over";
        window.onbeforeunload= null;
        return false;
    }
    var obj_list = jQuery.parseJSON(obj.results);
    var html_string = "";
    $(obj_list).each(function()
        {
            if (this.link != obj.url_to_find)
            {
                html_string+= "<Li><strong>" + this.title + "</strong></Li>";
            }
            else
            {
                html_string+= "<Li class='text-warning'><strong>" + "Page was retrieved in this rank" + "</strong></Li>";
            }
        }
    );
    $('#search-results-ol').html(html_string);

    var game_updates_html =  "<tr><td><h4> current score :</h4></td><td><h4>"+ obj.current_score +"</h4></td></tr>"+
                             "<tr><td><h4> round no :</h4></td><td><h4>"+ obj.no_round +"</h4></td></tr>" +
                             "<tr><td><h4>remaining rounds :</h4></td><td><h4>"+ obj.no_remaining_rounds +"</h4></td></tr>"+
                             "<tr><td><h4>queries issued for this page :</h4></td><td><h4>" +obj.no_of_queries_issued_for_current_page+ "</h4></td></tr>";
    $('#game_updates-div').html(game_updates_html);
    $('#score-div').html("<Strong>score :" + obj.score + "</strong>");
    $('#avatar-div').html("<h3>" + obj.avatar + "</h3>")
    if(obj.score != 0)
    {
        $('#skip-button').html("<i class='icon-forward icon-white'></i> take points");
        $('#skip-button').removeClass("btn-error").addClass("btn-success");
        $('#search-button').html('<i class="icon-search icon-white"></i> search again');
        $('#content-div').removeClass("alert-error").addClass("alert-success");
    }
    else
    {
        $('#skip-button').html("<i class='icon-forward icon-white'></i> skip");
        $('#skip-button').removeClass("btn-success").addClass("btn-danger");
        $('#search-button').html('<i class="icon-search icon-white"></i> search');
        $('#content-div').removeClass("alert-success").addClass("alert-error");
    }
    adjust_body_divs_height();
}

function display_next_page_success(data, textStatus, jqXHR)
{
    $('#query').val("");
    $('#query').focus();
    $('#content-div').removeClass("alert-success");
    $('#content-div').addClass("alert-error");
    $('#skip-button').removeClass("btn-success").addClass("btn-danger");
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.onbeforeunload= null;
        window.location ="/rmiyc/game_over";
        return false;
    }
    var game_updates_html =  "<tr><td><h4> current score :</h4></td><td><h4>"+ obj.current_score +"</h4></td></tr>"+
                             "<tr><td><h4> round no :</h4></td><td><h4>"+ obj.no_round +"</h4></td></tr>" +
                             "<tr><td><h4>remaining rounds :</h4></td><td><h4>"+ obj.no_remaining_rounds +"</h4></td></tr>"+
                             "<tr><td><h4>queries issued for this page :</h4></td><td><h4>" +obj.no_of_queries_issued_for_current_page+ "</h4></td></tr>";
    $('#game_updates-div').html(game_updates_html);
    $('#search-results-ol').html("");
    $('#score-div').html("");
    $('#skip-button').html("<i class='icon-forward icon-white'></i> skip");
    $('#search-button').html('<i class="icon-search icon-white"></i> search');
    $('#image-box').hide();
    $('#image-div').html("<image src= '" + obj.screenshot + "' height='1000' width='1000'> </image>");
    adjust_body_divs_height();
}

function adjust_header_divs_height()
{
    var highestCol = Math.max($('#statistics-div').height(),$('#header-div').height());
    $('#statistics-div').height(highestCol);
    $('#header-div').height(highestCol);
}

function adjust_body_divs_height()
{
    var search_div_height =$('#search-div').height();
    var content_div_height = $('#content-div').height();
    var search_div_margin =$('#search-div').css("margin-bottom");
    var variable =search_div_height + content_div_height;
    var highestCol = Math.max($('#image-div').height(),variable);
    if (highestCol < 650)
    {
        highestCol=650;
    }
    $('#image-div').height(highestCol);
    $('#content-div').height(highestCol - search_div_height - 35);
}

function adjust_search_input_width()
{
    var search_div_width =$('#search-div').width();
    $('#query').width(search_div_width -20);
}
function avatar()
{
        $('#search-div').fadeTo(0,0);
        $('#content-div').fadeTo(0,0);
        $('#image-div').fadeTo(0,0);
        $('#avatar-div').html("<h3> Ready? </h3>")
        timeoutID = window.setTimeout(avatar1, 2000);
}

function avatar1()
{
        timeoutID = window.setTimeout(avatar1, 2000);
        $('#search-div').fadeTo(1500,1);
        $('#content-div').fadeTo(1500,1);
        $('#image-div').fadeTo(1500,1);
        $('#avatar-div').html("<h3> if you retrieve the page, you can have the points!  </h3>")
        window.clearTimeout(timeoutID);
}

function initiate_game()
{
         var game_updates_html =  "<tr><td><h4> score :</h4></td><td><h4> 0 </h4></td></tr>"+
                             "<tr><td><h4> round no :</h4></td><td><h4> 1 </h4></td></tr>" +
                             "<tr><td><h4> remaining rounds :</h4></td><td><h4> 3 </h4></td></tr>"+
                             "<tr><td><h4> queries issued for this page :</h4></td><td><h4> 0 </h4></td></tr>";
         $('#game_updates-div').html(game_updates_html);
         avatar();
         adjust_header_divs_height();
         adjust_body_divs_height();
         adjust_search_input_width();
}