/**
 * Created by gabriele on 16/07/14.
 */



$(document).ready(function(){
    console.log("Ajax started");
    var pointer = $('#pointer').val();
    pointer *=1;
    $('.buttons').click(function(){

        var pos = $('#blockposition_'+pointer).val();
        var gold = $('#digbutton_'+pointer).val();
        console.log(pointer, "pointer");


        var csrf = $('#csrf > input').val();

        $('#invisiblebuttons_'+pointer).addClass("hidden");
        $('#movebutton_'+pointer).addClass("hidden");


        console.log(pos, "pos");
        console.log(gold, "gold");
        $.ajax({
            type: "POST",
            url: "/gold_digger/ajaxview/",
            data: {block: pos, dig: gold, csrfmiddlewaretoken: csrf},
            statusCode:{
            200: function(response){


                var points_pos = Math.floor((Math.random() * 500) + 1);
                console.log(points_pos, "poin position");
                var comment;

                if (response['goldextracted']>=0 && response['goldextracted']<5){
                    comment = ":(";
                }
                else if(response['goldextracted']>=5 && response['goldextracted']<10){
                    comment = "GOOD";
                }

                else if(response['goldextracted']>=10 && response['goldextracted']<15){
                    comment = "MONEY!";
                }

                else if (response['goldextracted']>=15 && response['goldextracted']<25){
                    comment = "CHICKEN DINNER!";
                }

                else if (response['goldextracted']>=25 && response['goldextracted']<30){
                    comment = "PAY DAY!";
                }

                else if (response['goldextracted']>=30 && response['goldextracted']<35){
                    comment = "SHINY!!";
                }

                else {
                    comment = "GOLD RUSH!!!";
                }

                console.log(comment, "comment");

                // Update points
                $('#totalgold').animateNumbers(response['totalgold'], true, 200, "linear");
                $('.progress-bar').css("width", response['timeremaining']+"%").html(response['timeremaining']+"%");
                $('#currentgold').animateNumbers(response['currentgold'], true, 200, "linear");

                // Update mine layer
                $('#goldlayer_'+pointer).removeClass().addClass("row nuggets_"+response['nuggets']);
                $('#scaffoldlayer_'+pointer).removeClass().addClass("scaffold_"+Math.floor((Math.random() * 3) + 1));
                $('#comment_'+pointer).html(comment).css('visibility', 'visible').animate({opacity: 1.0}, 300).fadeOut( "slow" );
                $('#points_'+pointer).html(response['goldextracted'] + " ").append('<img src="/static/nugget.png"/>').css("left", points_pos).css('visibility', 'visible').animate({opacity: 1.0, bottom: '70px'}, 300).animate({opacity: 0.0}, 300);
                $('#row_'+pointer).append("<div class='row' id='resultcol'>"+ gold +"<img src='/media/icons/Items/Gold.png'> ("+response['goldextracted']+")<img src='/media/icons/Items/Chest.png'>"+"</div>");

                pointer +=1;
                // Update side
                $('#invisiblebuttons_'+pointer).removeClass("hidden");
                $('#movebutton_'+pointer).removeClass("hidden");


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