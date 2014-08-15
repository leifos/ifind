/**
 * Created by 2108535R on 15/08/14.
 */

   $(document).ready(function(){
    console.log("Egg ajax started");
    $(".locationegg").click(function(){


        var csrf = $('#csrf > input').val();

        $.ajax({
           type: "POST",
           url: "/gold_digger/egg/",
           data: { csrfmiddlewaretoken: csrf },
           statusCode:{
            200: function(){
                $('#egg').modal('show')
            },

            204: function(){
                console.log("No egg")
            }

           }
           })
    })
});
