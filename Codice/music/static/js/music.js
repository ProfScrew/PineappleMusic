
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

$('#backsong').on('click', function () {
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0){
        backsong=$("#songnumber").val()-1;
        if(backsong<0)
            backsong=$("#maxsongnumber").val()-1;
        
        $("#coverplayer").attr("src", "https://drive.google.com/uc?export=view&id=" +$($($("#listsong[value='"+backsong+"']").parent().parent()).find("input")[0]).val());
        $("#title-song").text($($($("#listsong[value='"+backsong+"']").parent().parent()).find("td")[2]).text());
        $("#artist-song").text($($($("#listsong[value='"+backsong+"']").parent().parent()).find("td")[1]).text());
        $("#songnumber").val(backsong);
        $("#playerhidden").attr("src", "https://docs.google.com/uc?export=open&id=" + $($($("#listsong[value='"+backsong+"']").parent().parent()).find("input")[2]).val());
        if ($('#playpause').attr('class') == 'play-pause fas fa-play') {
            $("#playerhidden").trigger("pause");
        }
    }
});

$('#nextsong').on('click', function () {
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0){
        nextsong=$("#songnumber").val();
        nextsong++;
        if(nextsong==$("#maxsongnumber").val())
            nextsong=0;

        $("#coverplayer").attr("src", "https://drive.google.com/uc?export=view&id=" +$($($("#listsong[value='"+nextsong+"']").parent().parent()).find("input")[0]).val());
        $("#title-song").text($($($("#listsong[value='"+nextsong+"']").parent().parent()).find("td")[2]).text());
        $("#artist-song").text($($($("#listsong[value='"+nextsong+"']").parent().parent()).find("td")[1]).text());
        $("#songnumber").val(nextsong);
        $("#playerhidden").attr("src", "https://docs.google.com/uc?export=open&id=" + $($($("#listsong[value='"+nextsong+"']").parent().parent()).find("input")[2]).val());
        if ($('#playpause').attr('class') == 'play-pause fas fa-play') {
            $("#playerhidden").trigger("pause");
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
        $('#time-bar').attr('style', "width:" + document.getElementById("playerhidden").currentTime * 100 / document.getElementById("playerhidden").duration + "%;");
        $("#time-att").text(convert_to_time(document.getElementById("playerhidden").currentTime));
    }
}, 1000);

var old_volume=1.0

$("#icon-volume").on("click", function () {
        if ($('#icon-volume').attr('class') == 'fas fa-volume-down') {
            $('#icon-volume').attr('class', 'fas fa-volume-mute');
            old_volume = document.getElementById("playerhidden").volume;
            document.getElementById("playerhidden").volume = 0;
        } else {
            $('#icon-volume').attr('class', 'fas fa-volume-down');
            document.getElementById("playerhidden").volume = old_volume;
        }
});

$('.selectpicker').val('default').selectpicker('deselectAll');