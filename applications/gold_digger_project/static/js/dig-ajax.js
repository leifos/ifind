/**
 * Created by gabriele on 16/07/14.
 */
$(document).ready(function(){
    $('#digbutton').click(function(){
        var pos = $('#blockposition').val();
        var gold = $('#digbutton').val();

        var csrf = $('#csrf > input').val();
        $('#row_'+pos).addClass("hidden");

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajaxview/",
            data: {block: pos, dig: gold, csrfmiddlewaretoken: csrf},
            success: function(response){


                console.log(pos);
                $('#totalgold').html(response['totalgold']);
                $('#progressbar').css("width", response['timeremaining']);
                $('#currentgold').html(response['currentgold']);

                $('#goldlayer').removeClass().addClass("row nuggets_"+response['nuggets']);
                $('#scaffoldlayer').removeClass().addClass("scaffold_"+Math.floor((Math.random() * 3) + 1));
                $('#row_1').removeClass()

            }
        })
    })
})