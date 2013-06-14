$(document).ready(function(){

    $(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

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

$('#timer-label').hide()
$('#timer').html('')
$('label.user-info').append('</br></br><a href="/pagefetch/logout/">Logout</a>');
$('#results_view').remove();
$('#game_view').html('');

document.getElementById('red-border-game').id = "red-border-post-game"
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
$('#red-border-game').append("<div id='game_status'><img src='/site_media/pagefetch/GamePageImages/GO.png' alt='GO!'/></div>")
$('#game_status').flyOffPage({
direction: 'top',
duration:3500
});

$.ajax({
type: "POST",
url: "/pagefetch/game-form/",
success: function(game_result){
    $('#game_view').html(game_result);
    $('#query').focus();
    $('.error').hide();
    $('#spinner').hide();
    initialise_events();
}
});

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
    $('#query').focus();
    $('.error').hide();
    $('#spinner').hide();
    initialise_events();
}
});

return false;
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