/**
 * Created by gabriele on 16/07/14.
 */

var count = 0;
$(document).ready(function(){
    console.log("Ajax started");

    $('.buttons').click(function(){

        var pos = $('#blockposition_'+count).val();
        var gold = $('#digbutton_'+count).val();

        var csrf = $('#csrf > input').val();

        $('#invisiblebuttons_'+count).addClass("hidden");

        count += 1;
        console.log(count);
        console.log(pos);
        console.log(gold);
        $.ajax({
            type: "POST",
            url: "/gold_digger/ajaxview/",
            data: {block: pos, dig: gold, csrfmiddlewaretoken: csrf},
            success: function(response){



                console.log(count);
                $('#totalgold').html(response['totalgold']);
                $('#progressbar').css("width", response['timeremaining']);
                $('#currentgold').html(response['currentgold']);

                $('#goldlayer').removeClass().addClass("row nuggets_"+response['nuggets']);
                $('#scaffoldlayer').removeClass().addClass("scaffold_"+Math.floor((Math.random() * 3) + 1));
                $('#invisiblebuttons_'+count).removeClass("hidden");

            }
        })
    })
});