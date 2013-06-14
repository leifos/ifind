// When the document is ready re-size the images to be square - i.e. set size by adding margins
$(document).ready(function() 
{
	resizeImages();
	//$(".resultArea").refresh();
});

// Calculate what is missing to make it square
function resizeImages()
{
	$(".imageThumbnail").each(function()
	{
		var width = $(this).attr("width");
		var height = $(this).attr("height");
		var squareSize = 160;
		
		if (width < squareSize)
		{
			marginWidth = (squareSize - width) / 2;
		}
		else
		{
			marginWidth = 0;
		}
		
		if (height < squareSize)
		{
			marginHeight = (squareSize - height) / 2;
		}
		else
		{
			marginHeight = 0;
		}
		
		$(this).css("margin-left", marginWidth.toString() + 'px');
		$(this).css("margin-right", marginWidth.toString() + 'px');
		$(this).css("margin-top", marginHeight.toString() + 'px');
		$(this).css("margin-bottom", marginHeight.toString() + 'px');	
	});
}
