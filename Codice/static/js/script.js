$(".sidebar ul li").on('click', function () {
    $(".sidebar ul li.active").removeClass('active');
    $(this).addClass('active');
});

$('.open-btn').on('click', function () {
    $('.sidebar').addClass('active');
});

$('.close-btn').on('click', function () {
    $('.sidebar').removeClass('active');
});



$(document).ready(function () {
    $("#show_hide_password a").on('click', function (event) {
        event.preventDefault();
        if ($('#show_hide_password input').attr("type") == "text") {
            $('#show_hide_password input').attr('type', 'password');
            $('#show_hide_password i').removeClass("fa-regular");
            $('#show_hide_password i').addClass("fa-solid");

        } else if ($('#show_hide_password input').attr("type") == "password") {
            $('#show_hide_password input').attr('type', 'text');
            $('#show_hide_password i').removeClass("fa-solid");
            $('#show_hide_password i').addClass("fa-regular");
        }
    });
});

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

$(document).ready(function () {
    $('#example').DataTable({
        select: {
            style: 'single'
        },
        'columnDefs': [
            //hide the first and third column
            { 'visible': false, 'targets': [1, 6] }
        ]
    });
});

function convert_to_time(audioCurrentTime){
    var minutes = "0" + Math.floor(audioCurrentTime / 60);
    var seconds = "0" + Math.floor(audioCurrentTime - minutes * 60);
    return minutes.substr(-2) + ":" + seconds.substr(-2);
}

$(document).ready(function () {
    var table = $('#example').DataTable();

    $('#example tbody').on('click', 'tr', function () {
        var data = table.row(this).data();
        $("#coverplayer").attr("src", "https://drive.google.com/uc?export=view&id=" + data[1]);
        $("#title-song").text(data[2]);
        $("#playerhidden").attr("src", "https://docs.google.com/uc?export=open&id=" + data[6]);
        $("#playerhidden").trigger("play");
        $('#playpause').attr('class', 'fa fa-light fa-pause');

        $("#playerhidden").on('loadedmetadata', function() {
            var audioCurrentTime = document.getElementById("playerhidden").duration;
            
            $("#time-dur").text(convert_to_time(audioCurrentTime));
        });
    });
});


var interval = setInterval(function(){ 
    var audio=document.getElementById("playerhidden").duration;
    if (typeof ($('#playerhidden').attr('src')) != "undefined" && $('#playerhidden').attr('src').length > 0&&!isNaN(audio)){
            //console.log(document.getElementById("playerhidden").currentTime+" "+document.getElementById("playerhidden").duration);
            $('#time-bar').attr('style',"width:"+Math.trunc(document.getElementById("playerhidden").currentTime*100/document.getElementById("playerhidden").duration)+"%;");
            $("#time-att").text(convert_to_time(document.getElementById("playerhidden").currentTime));        
    }
  }, 1000);
