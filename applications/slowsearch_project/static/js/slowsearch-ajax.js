$(document).ready(function() {
    ajax_search();
    $("#throbber").html('<img alt="loading..." src="/img/throbber.gif" />').hide();
    $("#sendFormButton").click(function(e){
        e.preventDefault();
        ajax_search();
    });
});
