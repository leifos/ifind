/* Javascript logic for executing game logic
 * Based on the following sources:
 * "Submit A Form Without Page Refresh using jQuery" available at
 *  http://net.tutsplus.com/tutorials/javascript-ajax/submit-a-form-without-page-refresh-using-jquery/ 
*/

/* Loading spinner logic based on "How to create a Loading Animation/ Spinner using JQuery".
* Available at http://techscouting.wordpress.com/2010/11/08/how-to-create-a-loading-animation-spinner-using-jquery
* spinner.gif generated at http://ajaxload.info
*/

$(document).ready(function(){
$('#timer').spriteTimer({
'seconds': 180,
'isCountDown': true,
'digitImagePath': '/site_media/pagefetch/GamePageImages/numbers.png',
'callback': timer_finished
});
init_game_view();

return false;
});

function timer_finished()
{
var content = 'game_id=' + $("input#game_id").val();

$('#timer-div').hide()
$('#results_view').remove();
$('#game_view').html('');

document.getElementById('red-border-game-v2').id = "red-border-post-game"
document.getElementById('blue-border-game').id = "blue-border-post-game"

$.ajax({
type: "POST",
url: "/pagefetch/post_game/",
data: content,
success: function(post_content){
    $('#game_view').html(post_content);
    $('#play').click(function(event){
    event.preventDefault();
    window.location = "/pagefetch/play/"
    });
}
});     

return false;
}

function init_game_view()
{
$('#red-border-game-v2').append("<div id='game_status'><img src='/site_media/pagefetch/GamePageImages/GO.png' alt='GO!'/></div>")
$('#game_status').flyOffPage({
direction: 'top',
duration:3500
});

$.ajax({
type: "POST",
url: "/pagefetch/game-form/",
success: function(game_result){
    $('#game_view').html(game_result);
    $('.error').hide();
    $('#spinner').hide();
    initialise_events();
}
});

$('input#query').focus();

return false;
}

function get_game_view()
{
var content = 'game_id=' + $("input#game_id").val();

$.ajax({
type: "POST",
url: "/pagefetch/game-form/",
data: content,
success: function(game_result){
    $('#game_view').html(game_result);
    $('.error').hide();
    $('#spinner').hide();
    /*$('label#query_stuff').show();*/
    initialise_events();
}
});
}

function initialise_events()
{
$('#search_form').submit(function(event){
event.preventDefault();
$('#timer').trigger('stopTimer');
$('.error').hide();
$("#spinner").show();


var query_string = $("input#query").val();
    if (query_string == ""){
    $("label#query_error").show();
    $("input#query").focus();
    $("#spinner").hide();
    return false;
    }
    
var content = 'query='+ query_string + '&game_id=' + $("input#game_id").val();
$('#results_view').html('');
    
$.ajax({
type: "POST",
url: "/pagefetch/results/",
data: content,
success: function(result){
    $('#results_view').html(result);
    get_game_view();
    $("#spinner").hide();
    $('#timer').trigger('startTimer');
    
},
error: function(){
    $('#results_view').html('');
    $("#spinner").hide();
    
}
});
});

$('#continue').click(function(event){
event.preventDefault();
var content = 'game_id=' + $("input#game_id").val();
/*('label#query_stuff').hide();*/

$.ajax({
type: "POST",
url: "/pagefetch/get_next/",
data: content,
success: function(){
    $('#results_view').html('');
    get_game_view();
}
});
});
return false;
}