jQuery(document).ready(function($)
{
	var media_url = $('#media_url').text(); // Grab Django's site_media variable from an hidden div containing it for the image urls
	
	$( "#leftColumn, #rightColumn, #middleColumn" ).sortable(
	{
		connectWith: "#leftColumn, #rightColumn, #middleColumn",
		tolerence: "pointer",
		dropOnEmtpy: true,
		cursorAt: { cursor: "move", top: 0, left: 0 },
		over: function(event, ui) 
		{
			$(ui.helper).width($(this).find('.resultsBox').width());	
		},
		helper: function(event, ui) 
		{ 
			var myWidth = $(document).width() * 0.15;
			var myHeight = $(document).height() * 0.055;
            var id = '#' + $(ui).attr('id');
			var myHtml = $(id).find(".resultsBoxHeader").html();
            var myHelper = $('<div class="resultsBoxHelper"></div>');
            $(myHelper).html(myHtml);
			myHelper.height(myHeight);
			myHelper.width(myWidth);
			
			// If the colour is stored then add it
			if($.cookie("style"))
			{
				myColour = "white";
				
				if ($.cookie("style") == 'red')
				{					
					colour1 = "#FF0000";
					colour2 = "#F78383";
				}
				else if ($.cookie("style") == 'green')
				{
					colour1 = "#06C21C";
					colour2 = "#58BF64";
				}
				else if ($.cookie("style") == 'blue')
				{
					colour1 = "#003DF5";
					colour2 = "#00B8F5";
				}
				else if ($.cookie("style") == 'purple')
				{
					colour1 = "#4a0081";
					colour2 = "#cda3ed";
				}
				else if ($.cookie("style") == 'yellow')
				{
					myColour = "black";
					colour1 = "#fffd39";
					colour2 = "#f3f29d";
				}
				else if ($.cookie("style") == 'pink')
				{
					colour1 = "#f700e8";
					colour2 = "#ee8ae8";
				}
			}
			else
			{
				myColour = "white";
				colour1 = "#003DF5";
				colour2 = "#00B8F5";
			}			
			
			myHelper.css("color", myColour);
			myHelper.css("background", "-moz-linear-gradient(left,  " + colour1 + ",  " + colour2 + "");
			myHelper.css("background", "-webkit-gradient(linear, left top, right top, from(" + colour1 + "), to(" + colour2 + "))");
			return myHelper;
		},
		stop: function(event, ui) 
		{
			var leftIds = new Array();
			var middleIds = new Array();
			var rightIds = new Array();
			$("#leftColumn, #middleColumn, #rightColumn").find(".resultsBox").each(function()
			{
				var tempId = $(this).attr("id");
				
				if($(this).parent().attr("id") == 'leftColumn')
				{
					leftIds.push(tempId);
				}
				else if($(this).parent().attr("id") == 'middleColumn')
				{
					middleIds.push(tempId);
				}
				else if($(this).parent().attr("id") == 'rightColumn')
				{
					rightIds.push(tempId);
				}
				
				updateLeftColumn(leftIds);
				updateMiddleColumn(middleIds);
				updateRightColumn(rightIds);
				
			});
			
			resizeVideos();
			resizeImages();
			resizeColumns();
			$(this).find(".fullResults").fadeIn();
		},
	}).disableSelection();	
	
	
	function updateLeftColumn(leftIds)
	{
		$.cookie("leftColumn", leftIds, {expires: 365, path: '/'});
		return false;
	}
	
	function updateMiddleColumn(ids)
	{
		$.cookie("middleColumn", ids, {expires: 365, path: '/'});
		return false;
	}
	
	function updateRightColumn(rightIds)
	{
		$.cookie("rightColumn", rightIds, {expires: 365, path: '/'});
		return false;
	}
	
});