/**
 * Created by 2108535R on 05/08/14.
 */

$(document).ready(function () {
    $("button[name='upgrade_scan']").click(function () {
        $('#modal_s').modal('show');

        console.log("scan");
    });

    $("button[name='buyscan']").click(function(){
        console.log("buyscan")

        var csrf = $('#csrf > input').val();
        var up = "scan";

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajax_upgrade/",
            data: { up: up, csrfmiddlewaretoken: csrf },
            statusCode: {
                200: function (response) {

                    if(response['maxed_up'] == true){
                        $('#maxedout').modal('show');
                    }

                    else{
                    console.log("200");
                    $("#scan").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                    $("#gold").animateNumbers(response['gold'], true, 200, "linear");
                    }
                },

                204: function () {
                    console.log("No gold!");
                    $('#nogold').modal('show');
                     //("<div id='alert' class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Maxed out!!</strong></div>");
//                  $("#alert").animate({opacity: 0.0}, 2000);
//                  $("#message").delay( 800).remove();

                },

                202: function() {
                    console.log("No access to mine");
                    $('#noaccess').modal('show');
                }

            }
        })

   });


    $("button[name='upgrade_tool']").click(function () {
        $('#modal_t').modal('show');

        console.log("tool");

    });

    $("button[name='buytool']").click(function () {

        var csrf = $('#csrf > input').val();
        var up = "tool";

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajax_upgrade/",
            data: { up: up, csrfmiddlewaretoken: csrf },
            statusCode: {
                200: function (response) {
                    console.log("200");


                    if(response['maxed_up'] == true){
                        $('#maxedout').modal('show');
                    }

                    else {

                    $("#tool").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                    $("#gold").animateNumbers(response['gold'], true, 200, "linear");
                    }
                },

                204: function () {
                    console.log("No gold!");
                    $('#nogold').modal('show');
                     //("<div id='alert' class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Maxed out!!</strong></div>");
//                  $("#alert").animate({opacity: 0.0}, 2000);
//                  $("#message").delay( 800).remove();

                },

                202: function() {
                    console.log("No access to mine");
                    $('#noaccess').modal('show');
                }
            }
        })

        });


    $("button[name='upgrade_vehicle']").click(function () {
        console.log("vehicle");
        $('#modal_v').modal('show');

    });

    $("button[name='buyvehicle']").click(function () {

        var csrf = $('#csrf > input').val();
        var up = "vehicle";

        $.ajax({
            type: "POST",
            url: "/gold_digger/ajax_upgrade/",
            data: { up: up, csrfmiddlewaretoken: csrf },
            statusCode: {
                200: function (response) {

                    if(response['maxed_up'] == true){
                        $('#maxedout').modal('show');
                    }

                    else{

                    console.log("200");
                    $("#vehicle").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                    $("#gold").animateNumbers(response['gold'], true, 200, "linear");
                    }
                },

                204: function () {
                    console.log("No gold!");
                    $('#nogold').modal('show');
                     //("<div id='alert' class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Maxed out!!</strong></div>");
//                  $("#alert").animate({opacity: 0.0}, 2000);
//                  $("#message").delay( 800).remove();

                },

                202: function() {
                    console.log("No access to mine");
                    $('#noaccess').modal('show');
                }
            }
        })

    })

});

