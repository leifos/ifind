/**
 * Created by 2108535R on 27/07/14.
 */
$(document).ready(function(){
    console.log("Location ajax started");
    $(".location").click(function(){

        var loc = $(this).attr("title");
        var csrf = $('#csrf > input').val();

        $.ajax({
           type: "POST",
           url: "/gold_digger/update_location/",
           data: { loc: loc, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(){
                console.log("location changed")

            }
           }
           })
    })
});