$(document).ready(function () {
    if ($('.typed').length) {
        var typed = new Typed('.typed', {
            strings: ["Download entire YouTube playlists in just a few steps with YoutubeDownloader"],
            loop: true,
            typeSpeed: 100,
            backSpeed: 50,
            backDelay: 2000
        });
    }
});