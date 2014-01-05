$(document).ready(function()
{  
     $('.survey table tr').filter(':odd').addClass('odd');
	 $('.matrix ul').each(function() {
		$('li:first-child label input').css('float', 'right');
	  });

	  $('.addButton').toggle(function() {
      	  $('.hidden').css({display: 'inline'});
	  $(this).attr('value','-');
   	  return false;
	  }, function() {
      	  $('.hidden').css({display: 'none'});
	  $(this).attr('value','+');
   	  return false;
	   });


    $('.searchbox, .smallsearchbox').focus(function() {
        $.ajax({
            url: '/treconomics/query_focus/',
            dataType: 'json',
            error: function(data) {
                // If the experiment's time has been reached, we alert the user and redirect.
                var responseData = $.parseJSON(data.responseText);

                if ('timeout' in responseData) {
                    alert("Your time for this exercise has expired. We will now redirect you to the next step.");
                    window.location = APP_ROOT + 'next/';
                }
                else {
                    console.log("Server error on AJAX request: " + data.responseText);
                }
            }
        });
    });

    $('#end-task-link').click(function() {
        return confirm("Clicking OK will take you to the next stage of the experiment. If you clicked the 'End Task' link by accident, you can push the Cancel button below.");
    })

}); 


