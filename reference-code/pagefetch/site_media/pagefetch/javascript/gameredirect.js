/* Javascript logic for the status and leaderboard pages
 * Button redirects to a new game page
*/

$(document).ready(function(){
$('#play').click(function(event){
event.preventDefault();
window.location = "/pagefetch/categories/"
});
				  
$('#login-play').click(function(event){
event.preventDefault();
window.location = "/pagefetch/login/"
});				  
});
