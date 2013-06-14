jQuery(document).ready(function($)
{
	$("#titleEdit").hide();
	$("#searchEngineTitle").click(function()
	{
		$("#searchEngineTitle").hide();
		
		$("#titleEdit").attr("value", '');
		$("#titleEdit").show();
		$("#titleEdit").focus();
	});
	
	$('#titleEdit').keypress(function(e)
	{
		if(e.which == 13)
		{ // 13 = enter key
			$('#searchEngineTitle').text($("#titleEdit").attr("value"));
			$('#searchEngineName').attr("value", $("#titleEdit").attr("value"))
			$("#titleEdit").hide();
			$('#searchEngineTitle').show();
			
			// Create a cookie with the new title
			$.cookie("title", $("#searchEngineTitle").text(), {expires: 365, path: '/'});
		}
	});
});