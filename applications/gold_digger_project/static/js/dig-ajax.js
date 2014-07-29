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
            statusCode:{
            200: function(response){

                posi = count - 1;
                points_pos = Math.floor((Math.random() * 500) + 1);
                console.log(points_pos);
                var comment;

                if (response['goldextracted']>=0 && response['goldextracted']<5){
                    comment = "OK";
                }
                else if(response['goldextracted']>=5 && response['goldextracted']<10){
                    comment = "GOOD";
                }

                else if(response['goldextracted']>=10 && response['goldextracted']<15){
                    comment = "MONEY!";
                }

                else if (response['goldextracted']>=15 && response['goldextracted']<25){
                    comment = "YIPPIKAYAY!";
                }

                else if (response['goldextracted']>=25 && response['goldextracted']<30){
                    comment = "AWESOME!";
                }

                else if (response['goldextracted']>=30){
                    comment = "SHINY!!";
                }

                else {
                    comment = "GOLD RUSH!!!";
                }

                console.log(comment, "comment")

                $('#totalgold').animateNumbers(response['totalgold'], true, 200, "linear");
                $('.progress-bar').css("width", response['timeremaining']+"%").html(response['timeremaining']+"%");
                $('#currentgold').animateNumbers(response['currentgold'], true, 200, "linear");

                $('#goldlayer_'+posi).removeClass().addClass("row nuggets_"+response['nuggets']);

                $('#scaffoldlayer_'+posi).removeClass().addClass("scaffold_"+Math.floor((Math.random() * 3) + 1));
                $('#invisiblebuttons_'+count).removeClass("hidden");
                $('#movebutton_'+count).removeClass("hidden");
                $('#comment_'+posi).html(comment).css('visibility', 'visible').animate({opacity: 1.0}, 100).fadeOut( "fast" );
                $('#points_'+posi).html(response['goldextracted'] + " ").append('<img src="/static/nugget.png"/>').css("left", points_pos).css('visibility', 'visible').animate({opacity: 1.0, bottom: '70px'}, 300).animate({opacity: 0.0}, 300);
                $('#row_'+posi).append("<div class='row' id='resultcol'>"+ gold +"<img src='/media/icons/Items/Gold.png'> ("+response['goldextracted']+")<img src='/media/icons/Items/Chest.png'>"+"</div>");

                if (response['nextmine']){
                    $('.row #resultcol').append("<a class='blink_me' href='/gold_digger/move/'>Next mine?</a><br>");
                }



            },

            204: function (){
                window.location = "/gold_digger/game_over/"
            }

            }
        });
    });
});