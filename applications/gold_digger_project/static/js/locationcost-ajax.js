$(document).ready(function(){
    console.log("Cost ajax started");

    $(".btn.btn-primary").click(function(){
        var loc = $(this).val();
        var csrf = $('#csrf > input').val();
        var cost = 0;

        alert(loc);

        if (loc == 'California'){
            cost = 20
        }

        else if (loc == 'Yukon'){
            cost = 40
        }

        else if (loc == 'Brazil'){
            cost = 80
        }

        else if (loc == 'South Africa'){
            cost = 100
        }

        else if (loc == 'Scotland'){
            cost = 120
        }

        else if (loc == 'Victoria'){
            cost = 200
        }

        alert(cost);
        $.ajax({
           type: "POST",
           url: "/gold_digger/update_cost/",
           data: { cost: cost, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(){
                console.log("cost deducted");
                $(".totalgold").html("poooooopppppp")

            },

            204: function () {
                window.location = "/gold_digger/game_over2/";
                console.log("Game over man");
                alert("game over man")
            }


           }
           })
    });

});
