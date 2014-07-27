/**
 * Created by 2108535R on 25/07/14.
 */
$(document).ready(function(){
   $("button[name='buy equipment']").click(function(){
       var scan = $(this).val();

       var id = $(this).attr("id");

       alert(id);


       var csrf = $('#csrf > input').val();


       $.ajax({
           type: "POST",
           url: "/gold_digger/ajax_buy/",
           data: { scan: scan, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(response){

                $("#response_e"+id).append("<div class='alert alert-dismissable alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>");
                $("#scan").attr('src', response['image'])
                $("#gold").html('Gold: '+response['gold'])
            },

            204: function(){
                $("#response_e"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>")

            }
           }
       })
   });

    $("button[name='buy tool']").click(function(){
       var tool = $(this).val();

       var id = $(this).attr("id");

       alert(id);


       var csrf = $('#csrf > input').val();


       $.ajax({
           type: "POST",
           url: "/gold_digger/ajax_buy/",
           data: { tool: tool, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(response){

                $("#response_t"+id).append("<div class='alert alert-dismissable alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>");
                $("#tool").attr('src', response['image'])
                $("#gold").html('Gold: '+response['gold'])

            },

            204: function(){
                $("#response_t"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>")

            }
           }
       })
   });

    $("button[name='buy vehicle']").click(function(){
       var vehicle = $(this).val();

       var id = $(this).attr("id");

       alert(id);


       var csrf = $('#csrf > input').val();


       $.ajax({
           type: "POST",
           url: "/gold_digger/ajax_buy/",
           data: { vehicle: vehicle, csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(response){

                $("#response_v"+id).append("<div class='alert alert-dismissable alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>");
                $("#vehicle").attr('src', response['image'])
                $("#gold").html('Gold: '+response['gold'])

            },

            204: function(){
                $("#response_v"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>")

            }
           }
       })
   });
});