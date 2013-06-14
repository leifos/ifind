$(window).resize(function()
{
	resizeColumns();
});

// This method ensures all the columns fill the whole area available
function resizeColumns()
{
	// docHeight is the full height of the document - the header height
	var docHeight = $(document).height() - $("#header").height();
	$(".resultArea").height(docHeight);	
}