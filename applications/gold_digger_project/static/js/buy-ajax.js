/**
 * Created by 2108535R on 25/07/14.
 */
$(document).ready(function(){
   $("button[name='buy equipment']").click(function(){

       var scan = $(this).val();
       var id = $(this).attr("id");
       var csrf = $('#csrf > input').val();
       $("#scan").removeClass("fadeInRight");

       $.ajax({
           type: "POST",
           url: "/gold_digger/ajax_buy/",
           data: { scan: scan, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(response){

                $("#response_e"+id).append("<div class='alert alert-dismissable alert-success animated baunceInTop'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>").animate({opacity: 0.0}, 2000);
                $("#scan").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                $("#gold").animateNumbers(response['gold'], true, 200, "linear");
            },

            204: function(){
                $("#response_e"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>").animate({opacity: 0.0}, 2000);

            }
           }
       })
   });

    $("button[name='buy tool']").click(function(){

       var tool = $(this).val();
       var id = $(this).attr("id");
       var csrf = $('#csrf > input').val();
       $("#tool").removeClass("fadeInRight");

       $.ajax({
           type: "POST",
           url: "/gold_digger/ajax_buy/",
           data: { tool: tool, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(response){

                $("#response_t"+id).append("<div class='alert alert-dismissable alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>").animate({opacity: 0.0}, 2000);
                $("#tool").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                $("#gold").html('Gold: '+response['gold']);

            },

            204: function(){
                $("#response_t"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>").animate({opacity: 0.0}, 2000);

            }
           }
       })
   });

    $("button[name='buy vehicle']").click(function(){

       var vehicle = $(this).val();
       var id = $(this).attr("id");
       var csrf = $('#csrf > input').val();
       $("#vehicle").removeClass("fadeInRight");


       $.ajax({
           type: "POST",
           url: "/gold_digger/ajax_buy/",
           data: { vehicle: vehicle, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(response){

                $("#response_v"+id).append("<div class='alert alert-dismissable alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>").animate({opacity: 0.0}, 2000);
                $("#vehicle").attr('src', response['image']).addClass("animated").addClass("fadeInRight");
                $("#gold").html('Gold: '+response['gold']);

            },

            204: function(){
                $("#response_v"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>").animate({opacity: 0.0}, 2000);

            }
           }
       })
   });
});