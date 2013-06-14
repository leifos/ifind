// When the document is ready re-size the videos iframes to fit the size of their containing element
$(document).ready(function() 
{
	resizeVideos();
});

// If the window is resized we need to resize the iframes
$(window).resize(function()
{
	resizeVideos();
});

// Take the size of the video results div and calculate the width and height based on it
function resizeVideos()
{
	$(".embeddedVideo").each(function()
	{
		var width = $("#videoResults").width() - 50;
		var height = 9/16 * width + 25; // 25px for the video controls
		$(this).attr("width", width.toString() + 'px');
		$(this).attr("height", height.toString() + 'px');	
	});
}
