$(function()
{
    window.onbeforeunload = confirmExit;
    function confirmExit()
    {
        return false;
    }

    $(document).keypress(function(event)
    {
        if(event.which == 13 && event.ctrlKey)
        {
            event.preventDefault();
            $.ajax
            ({
                type: "GET",
                url: "/rmiyc/display_next_page/",
                success: display_next_page_success,
                dataType: 'html'
            });
        }
    });

    $('#search_form').submit(function(event)
    {
        event.preventDefault();
        $.ajax
        ({
            type: "POST",
            url: "/rmiyc/search/",
            data:
            {
                'query' : $('#query').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: search_success,
            dataType: 'html'
        });

    });

    $('#skip').click(function(event)
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
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.location ="/rmiyc/game_over";
        window.onbeforeunload= null;
        return false;
    }
    var obj_list = jQuery.parseJSON(obj.results);
    var html_string = ""
    $(obj_list).each(function()
        {
            html_string+= "<Li> <b>" + this.title + "</b> <br />" +this.link +"</Li>";
        }
    );
    $('#num-queries').html("<p>you have issued :" + obj.no_of_queries_issued_for_current_page+" queries for this web page</p> <br />");
    $('#game_updates').html("<p>you have <strong> played : " +  obj.no_round + " rounds </strong>, " + obj.no_successful_round +
        " were completed successfully. <br />" +
        "you have" + obj.no_remaining_rounds + " remaining rounds </p>");
    $('#search-results-ol').html(html_string);
    $('#score-div').html("<h4>your score is :" + obj.score + "</h4>");
    $('#query').val("");
    if(obj.score != 0)
    {
        $('#skip').text('take points');
        $('#search').text('search again');
    }
    else
    {
        $('#skip').text('skip');
        $('#search').text('search');
    }
}

function display_next_page_success(data, textStatus, jqXHR)
{
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.location ="/rmiyc/game_over";
        window.onbeforeunload= null;
        return false;
    }
    $('#num-queries').html("<p>you have issued :" + obj.no_of_queries_issued_for_current_page+" queries for this web page</p> <br />");
    $('#game_updates').html("<p>you have <strong> played : " +  obj.no_round + " rounds </strong>, " + obj.no_successful_round +
        " were completed successfully. <br />" +
        "you have" + obj.no_remaining_rounds + " remaining rounds </p>");

    $('#search-results-ol').html("");
    $('#score-div').html("");
    $('#skip').text('skip');
    $('#search').text('search');
    $('#image-box').hide();
    $('#image-div').html("<image src= '" + obj.screenshot + "' height='1000' width='1000'> </image>");
}