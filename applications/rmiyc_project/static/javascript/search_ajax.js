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
    $('#content').html(data);
    $('#query').val("");
    var x = $('#score-variable').text();
    if(x!= 0)
    {
        $('#skip').text('take points');
        $('#search').text('search again');
    }
}

function display_next_page_success(data, textStatus, jqXHR)
{
    $('#skip').text('skip');
    $('#search').text('search');
    $('#image-box').hide();
    $('#score-div').hide();
    $('#search-results-div').hide();
    $('#image-div').html(data);
}