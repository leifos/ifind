/* Function responsible for rendering login
or directing straight to game
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