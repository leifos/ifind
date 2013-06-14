// When the document is ready check if we have a cookie containing the users settings
$(document).ready(function() 
{ 
	if($.cookie("leftColumn"))
	{
		var ids = $.cookie("leftColumn").split(",");
		ids.reverse();

		for (i = 0; i < ids.length; i++)
		{
			var newId = '#' + ids[i];
			var test = $(newId);

			if (test.length == 1)
			{
				$(test).remove();
				$("#leftColumn").prepend($(test));
			}
		}
	}
	
	if($.cookie("middleColumn"))
	{
		var ids = $.cookie("middleColumn").split(",");
		ids.reverse();

		for (i = 0; i < ids.length; i++)
		{
			var newId = '#' + ids[i];
			var test = $(newId);

			if (test.length == 1)
			{
				$(test).remove();
				$("#middleColumn").prepend($(test));
			}
		}
	}
	
	if($.cookie("rightColumn"))
	{
		
		var ids = $.cookie("rightColumn").split(",");
		ids.reverse();
		
		
		for (i = 0; i < ids.length; i++)
		{
			var newId = '#' + ids[i];
			var test = $(newId);

			if (test.length == 1)
			{
				$(test).remove();
				$("#rightColumn").prepend($(test));
			}
		}

	}
	
	// If the title is stored then add it
	if($.cookie("title"))
	{
		$("#searchEngineTitle").text($.cookie("title"));
	}
	
	// If the colour is stored then add it
	if($.cookie("style"))
	{
		if ($.cookie("style") == 'red')
		{
			applyStyle("#f89c9c", "#FF0000" , "#FFFFFF", "#FF0000" , "#F78383");
		}
		else if ($.cookie("style") == 'green')
		{
			applyStyle("#88bd8e", "#06C21C", "#FFFFFF", "#06C21C" , "#58BF64");
		}
		else if ($.cookie("style") == 'blue')
		{
			applyStyle("#78d1ee", "#003DF5", "#FFFFFF", "#003DF5" , "#00B8F5");
		}
		else if ($.cookie("style") == 'purple')
		{
			applyStyle("#dac4ea", "#4a0081", "#FFFFFF", "#4a0081" , "#cda3ed");
		}
		else if ($.cookie("style") == 'yellow')
		{
			applyStyle("#f0efb2", "#000000", "#000000", "#fffd39", "#f3f29d");
		}
		else if ($.cookie("style") == 'pink')
		{
			applyStyle("#e9a7e5", "#f700e8", "#FFFFFF", "#f700e8" , "#ee8ae8");
		}
	}
	
	function applyStyle(bodyBackgroundColour, queryTextColour, myColour, colour1, colour2)
	{
		$("#searchEngineTitle").css("color", myColour);

		$("body").css("background-color", bodyBackgroundColour);
		$('#query').css('color', queryTextColour);

		$("#header").css("color", myColour);
		$("#header").css("background", "-moz-linear-gradient(left,  " + colour1 + ",  " + colour2 + ")");
		$("#header").css("background", "-webkit-gradient(linear, left top, right top, from(" + colour1 + "), to(" + colour2 + "))");
		
		$(".resultsBoxHeader").css("color", myColour);
		$(".resultsBoxHeader").css("background", "-moz-linear-gradient(left,  " + colour1 + ",  " + colour2 + "");
		$(".resultsBoxHeader").css("background", "-webkit-gradient(linear, left top, right top, from(" + colour1 + "), to(" + colour2 + "))");
		
		$(".resultsBoxOptions").css("color", myColour);
		$(".resultsBoxOptions").css("background", "-moz-linear-gradient(left,  " + colour1 + ",  " + colour2 + ")");
		$(".resultsBoxOptions").css("background", "-webkit-gradient(linear, left top, right top, from(" + colour1 + "), to(" + colour2 + "))");
	}
	
	$(".changeStyle").click(function()
	{ 
		$.cookie("style", $(this).attr('rel'), {expires: 365, path: '/'});
		
		if ($(this).attr('rel') == 'red')
		{
			applyStyle("#f89c9c", "#FF0000" , "#FFFFFF", "#FF0000" , "#F78383");
		}
		else if ($(this).attr('rel') == 'green')
		{
			applyStyle("#88bd8e", "#06C21C", "#FFFFFF", "#06C21C" , "#58BF64");
		}
		else if ($(this).attr('rel') == 'blue')
		{
			applyStyle("#78d1ee", "#003DF5", "#FFFFFF", "#003DF5" , "#00B8F5");
		}
		else if ($(this).attr('rel') == 'purple')
		{
			applyStyle("#dac4ea", "#4a0081", "#FFFFFF", "#4a0081" , "#cda3ed");
		}
		else if ($(this).attr('rel') == 'yellow')
		{
			applyStyle("#f0efb2", "#000000", "#000000", "#fffd39" , "#f3f29d");
		}
		else if ($(this).attr('rel') == 'pink')
		{
			applyStyle("#e9a7e5", "#f700e8", "#FFFFFF", "#f700e8" , "#ee8ae8");
		}
		
		return false;

	});	
	
});