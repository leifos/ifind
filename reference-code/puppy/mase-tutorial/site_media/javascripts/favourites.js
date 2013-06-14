$(document).ready(function()
{ 	
	if($.cookie("favourites"))
	{
		var favourites = $.cookie("favourites").split(",");
		renderFavourites(favourites);
	}
});

function addFavourite()
{
	var favourite = $("#query").attr("value");
	var favourites = [];
	var found = false;
	
	if (favourite != '' && favourite !=' ')
	{
		
		$('.favourite').each(function() 
		{
			var tempFavourite = $(this).text();
			
			if (favourite == tempFavourite)
			{
				found = true; // We don't want duplicates
			}
			
			favourites.push(tempFavourite);
		});
	
		if (found == false) // If it's a new favourite add it to the list of favourites
		{
			favourites.push(favourite);
			$.cookie("favourites", favourites, {expires: 365, path: '/'});	
       		renderNewFavourite(favourite);
		}
	
	}
}

function removeFavourite(removeFavourite)
{
	console.log(removeFavourite);
	var deleteFavourite = $(removeFavourite).parent().remove();
	var favourites = [];
	
	$('.favourite').each(function() 
	{
		favourites.push($(this).text());
	});
	
	$.cookie("favourites", favourites, {expires: 365, path: '/'});
	renderFavourites(favourites);
}

function renderNewFavourite(favourite)
{
	var results_html = $("#myFavourites").html();

	var newFav = '<p class="favouriteEntry"><a href="?query=' + favourite + '" class="favourite">' + favourite + '</a><a href = "#" onclick="javascript: removeFavourite(this)" class="deleteFav">X</a></p>';
	results_html = results_html + newFav;
	
  	// update innerHTML of #resultbox
  	$("#myFavourites").html(results_html);
}

function renderFavourites(favourites)
{
	var results_html = '';

	for(index in favourites) 
	{
		var newFav = '<p class="favouriteEntry"><a href="?query=' + favourites[index] + '" class="favourite">' + favourites[index] + '</a><a href = "#" onclick="javascript: removeFavourite(this)" class="deleteFav">X</a></p>';
		results_html = results_html + newFav;
		
	}
  	// update innerHTML of #resultbox
  	$("#myFavourites").html(results_html);
}