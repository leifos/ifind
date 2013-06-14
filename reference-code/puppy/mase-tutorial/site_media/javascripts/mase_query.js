// This method grabs details of the window and adds them to the http POST inputs then submits the form
function submitNewMaseQuery(myQuery)
{
	$("#query").attr("value", myQuery);
	submitMaseQuery();	
}

function submitMaseQuery()
{
	$("#searchForm").submit();
}