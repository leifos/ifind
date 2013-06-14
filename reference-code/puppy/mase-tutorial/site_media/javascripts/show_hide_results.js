function show_hide_results(thisButton) 
{
	var resultBox = $(thisButton).parent().parent();
			
	$(resultBox).find('.fullResults').each(function(i)
	{			
		if ( $(this).is(':hidden') ) 
		{ 
	       	$(this).fadeIn();
	        resizeImages();
		}
		else
		{
			$(this).hide();
		}
		
	});
			
	if ( $(resultBox).find('.fullResults').is(':hidden') == false ) 
	{ 
				
		$(resultBox).css('border-bottom-width', '4px');
		$(thisButton).text("-");
				
		var header = $(resultBox).find('.resultsBoxHeader');
		$(header).css('border-top-right-radius', '10px');
		$(header).css('border-top-left-radius', '10px');
		$(header).css('border-radius', '');
				
	}
	else
	{
		$(resultBox).css('border-bottom-width', '0px');
		$(thisButton).text("+");
				
		var header = $(resultBox).find('.resultsBoxHeader');
		$(header).css('border-bottom-right-radius', '10px');
		$(header).css('border-bottom-left-radius', '10px');
			
	}	
}