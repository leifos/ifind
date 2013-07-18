$(function()
{
    window.onbeforeunload = confirmExit;
    function confirmExit()
    {
        return false;
    }

    $(document).keypress(function(event)
    {
        if(event.ctrlKey && event.which == 13)
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


    $('#search').click(function(event)
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
    $('#num-queries').html("<strong>no queries issued for this page : " + obj.no_of_queries_issued_for_current_page + "</strong>");
    $('#game_updates').html("<strong> round no : " +  obj.no_round + "  <br /> " +
        "remaining rounds : " + obj.no_remaining_rounds + "</strong>");

    $('#search-results-ol').html(html_string);
    $('#score-div').html("<h4>your score is :" + obj.score + "</h4>");
    $('#query').val("");
    if(obj.score != 0)
    {
        $('#skip').html("<i class='icon-forward icon-white'></i> take points");
        $('#skip').removeClass("btn-error").addClass("btn-success");
        $('#search').html('<i class="icon-search icon-white"></i> search again');
        $('#content').removeClass("alert-error").addClass("alert-success");
    }
    else
    {
        $('#skip').html("<i class='icon-forward icon-white'></i> skip");
        $('#skip').removeClass("btn-success").addClass("btn-danger");
        $('#search').html('<i class="icon-search icon-white"></i> search');
        $('#content').removeClass("alert-success").addClass("alert-error");
    }
}

function display_next_page_success(data, textStatus, jqXHR)
{
    var obj = jQuery.parseJSON(data);
    if (obj.is_game_over == 1)
    {
        window.onbeforeunload= null;
        window.location ="/rmiyc/game_over";
        return false;
    }

    $('#num-queries').html("<strong>no queries issued for this page : " + obj.no_of_queries_issued_for_current_page + "</strong>");
    $('#game_updates').html("<strong>round no : " +  obj.no_round + "  <br /> " +
        "remaining rounds : " + obj.no_remaining_rounds + "</strong>");

    $('#search-results-ol').html("");
    $('#score-div').html("");
    $('#skip').html("<i class='icon-forward icon-white'></i> skip");
    $('#search').html('<i class="icon-search icon-white"></i> search');
    $('#image-box').hide();
    $('#image-div').html("<image src= '" + obj.screenshot + "' height='1000' width='1000'> </image>");
}