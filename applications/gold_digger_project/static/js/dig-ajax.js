/**
 * Created by gabriele on 16/07/14.
 */
$(document).ready(function(){
    $('#digbutton').click(function(){
        var pos = $('#blockposition').val();
        var gold = $('#digbutton').val();
        var cue = $('goldlayer').val();

        var csrf = $('#csrf > input').val();

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajaxview/",
            data: {block: pos, dig: gold, csrfmiddlewaretoken: csrf},
            success: function(response){

                $('#totalgold').html(response['totalgold']);
                $('#progressbar').css("width", response['timeremaining']);
                $('#currentgold').html(response['currentgold']);

                $('#goldlayer').removeClass().addClass("row nuggets_"+response['nuggets']);
                $('#scaffoldlayer').removeClass().addClass("scaffold_"+Math.floor((Math.random() * 3) + 1));
//                $('#buttons').remove().

            }
        })
    })
})