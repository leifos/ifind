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

                $("#response_"+id).append("<div class='alert alert-dismissable alert-success'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Good job!</strong> Item purchased!</div>");

            },

            204: function(){
                $("#response_"+id).append("<div class='alert alert-dismissable alert-danger'><button type='button' class='close' data-dismiss='alert'>×</button><strong>Oh snap!</strong> Not enough gold!</div>")
            }
           }
       })
   });
});