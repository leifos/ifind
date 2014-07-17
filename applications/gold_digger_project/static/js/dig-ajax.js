/**
 * Created by gabriele on 16/07/14.
 */
$(document).ready(function(){
    $('#digbutton').click(function(){
        var pos = $('#blockposition').val();
        var gold = $('#digbutton').val();

        var csrf = $('#csrf > input').val();

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajaxview/",
            data: {block: pos, dig: gold, csrfmiddlewaretoken: csrf},
            success: function(response){
                alert(response['gold_dug']);
                $('#totalgold').html(response['totalgold']);
                $('#progressbar').css("width", response['timeremaining']);
                $('#currentgold').html(response['currentgold']);
                $('#')


            }
        })
    })
})