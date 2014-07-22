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
        $('#movebutton_'+count).addClass("hidden");
        count += 1;
        console.log(count);
        console.log(pos);
        console.log(gold);
        $.ajax({
            type: "POST",
            url: "/gold_digger/ajaxview/",
            data: {block: pos, dig: gold, csrfmiddlewaretoken: csrf},
            success: function(response){

                posi = count - 1;

                console.log(count);
                if (response['timeremaining'] <= 0){
                    $('.buttons').wrap("<form action='/gold_digger/game_over'></form>")
                }

                $('#totalgold').html(response['totalgold']);
                $('.progress-bar').css("width", response['timeremaining']+"%").html(response['timeremaining']+"%");
                $('#currentgold').html(response['currentgold']);

                $('#goldlayer_'+posi).removeClass().addClass("row nuggets_"+response['nuggets']);

                $('#scaffoldlayer_'+posi).removeClass().addClass("scaffold_"+Math.floor((Math.random() * 3) + 1));
                $('#invisiblebuttons_'+count).removeClass("hidden");
                $('#movebutton_'+count).removeClass("hidden");
                $('#row_'+posi).append("<div class='row' id='resultcol'>"+ gold +"<img src='/media/icons/Items/Gold.png'> ("+response['goldextracted']+")<img src='/media/icons/Items/Chest.png'>"+"</div>");

                if (response['nextmine']){
                    $('#well').append("<a class='blink_me' href='/gold_digger/move/'>Next mine?</a><br>");
                }



            }
        });
    });
});