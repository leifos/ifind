/**
 * Created by 2108535R on 05/08/14.
 */

$(document).ready(function () {
    $("button[name='upgrade_scan']").click(function () {
        console.log("scan");
        var csrf = $('#csrf > input').val();
        var up = "scan";

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajax_upgrade/",
            data: { up: up, csrfmiddlewaretoken: csrf },
            statusCode: {
                200: function (response) {
                    console.log("200");
                    $("#scan").append("<div class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>").animate({opacity: 0.0}, 2000);
                    $("#scan").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                    $("#gold").animateNumbers(response['gold'], true, 200, "linear");
                },

                204: function () {
                    console.log("maxed up!!!");
                    $("#playstore").append("<div id='alert' class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Maxed out!!</strong></div>");

                     //("<div id='alert' class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Maxed out!!</strong></div>");
//                  $("#alert").animate({opacity: 0.0}, 2000);
//                  $("#message").delay( 800).remove();

                }
            }
        })


    })

});