/**
 * Created by gabriele on 13/08/14.
 */

$(document).ready(function () {
    console.log("achievement ajax");

    var csrf = $('#csrf > input').val();
    console.log("achievement check");

    $.ajax({
        type: "POST",
        url: "/gold_digger/achievements/",
        data: {csrfmiddlewaretoken: csrf},
        statusCode: {
            200: function (response) {
                if (response['unlocked'] == true) {
                    console.log("No achievement")
                }
                else {
                    console.log("Achievement unlocked " + response['achievement_name']);
                    $('#achname').html(response['achievement_name']);
                    console.log(response['achievement_condition']);
                    $('#achcond').html(response['achievement_condition']);
                    $('#achimage').attr('src', response['achievement_image']);
                    $('#achdesc').html(response['achievement_desc']);
                    $('#achievement').modal('show')
                }
            },

            204: function () {
                console.log("No achievement")
            }

        }

    });

});