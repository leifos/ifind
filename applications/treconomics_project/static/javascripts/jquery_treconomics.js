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

}); 


