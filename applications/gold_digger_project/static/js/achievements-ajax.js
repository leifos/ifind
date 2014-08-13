/**
 * Created by gabriele on 13/08/14.
 */
$(document).ready(function (){

    var csrf = $('#csrf > input').val();


    $.ajax({
            type: "POST",
            url: "/gold_digger/achievements/",
            data: {csrfmiddlewaretoken: csrf},
            statusCode:{
            200: function(response){

            },

            204: function(response){
            }

            }

    });

    });