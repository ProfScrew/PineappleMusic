
$('#playpause').on('click', function () {
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0) {
        if ($('#playpause').attr('class') == 'play-pause fas fa-play') {
            $("#playerhidden").trigger("play");
            $('#playpause').attr('class', 'fa fa-light fa-pause');
        } else {
            $("#playerhidden").trigger("pause");
            $("#time-att").text(convert_to_time(document.getElementById("playerhidden").currentTime));
            $('#playpause').attr('class', 'play-pause fas fa-play');
        }
    }

});

$('#repeatsong').on('click', function () {
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0) {
        document.getElementById("playerhidden").currentTime = 0;
        $("#time-att").text(convert_to_time(document.getElementById("playerhidden").currentTime));
    }

});

function convert_to_time(audioCurrentTime) {
    var minutes = "0" + Math.floor(audioCurrentTime / 60);
    var seconds = "0" + Math.floor(audioCurrentTime - minutes * 60);
    return minutes.substr(-2) + ":" + seconds.substr(-2);
}




var interval = setInterval(function () {
    var audio = document.getElementById("playerhidden").duration;
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0 && !isNaN(audio)) {
        //console.log(document.getElementById("playerhidden").currentTime+" "+document.getElementById("playerhidden").duration);
        $('#time-bar').attr('style', "width:" + document.getElementById("playerhidden").currentTime * 100 / document.getElementById("playerhidden").duration + "%;");
        $("#time-att").text(convert_to_time(document.getElementById("playerhidden").currentTime));
    }
}, 1000);


$("#icon-volume").on("click", function () {
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0) {
        if ($('#icon-volume').attr('class') == 'fas fa-volume-down') {
            $('#icon-volume').attr('class', 'fas fa-volume-mute');
            document.getElementById("playerhidden").volume = 0;
        } else {
            $('#icon-volume').attr('class', 'fas fa-volume-down');
            document.getElementById("playerhidden").volume = 1.0;
        }
    }
});

$('.selectpicker').val('default').selectpicker('deselectAll');