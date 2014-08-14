/**
 * Created by 2108535R on 08/08/14.
 */



$(document).ready(function () {
var csrf = $('#csrf > input').val();

    $('#exitleader').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("leaderboards");
            window.location = "/gold_digger/leaderboards/";
            var escape = "leaderboards";

            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })

        });
    });

    $('#exitabout').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("about");
            window.location = "/gold_digger/about/";
            var escape = "about";
            console.log("exitlog");
            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })
        });
    });

    $('#exithowto').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("howto");
            window.location = "/gold_digger/tour/";
            var escape = "howto";

            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })

        });
    });

    $('#exitplay').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("play");
            window.location = "/gold_digger/game_choice2/";
            var escape = "play";

            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })
        });
    });

    $('#exithome').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("home");
            window.location = "/gold_digger/";
            var escape = "home";

            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })
        });
    });

     $('#exitprofile').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("profile");
            window.location = "/gold_digger/profile/";
            var escape = "profile";

            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })
        });
    });

    $('#exitachievements').click(function () {
        $('#exitpage').modal('show');

        $("button[name='goaway']").click(function () {
            console.log("profile");
            window.location = "/gold_digger/profile/";
            var escape = "profile";

            $.ajax({
                type: "POST",
                url: "/gold_digger/ajax_exit/",
                data: { escape: escape, csrfmiddlewaretoken: csrf },
                statusCode: {
                    200: function () {
                        console.log("exited")
                    }
                }
            })
        });
    });

});