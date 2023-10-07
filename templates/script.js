$(document).ready(function() {
    // Populate famous songs and new releases (you need to fetch this data from your backend)
    // Example data fetching using AJAX:
    // $.ajax({
    //     url: 'backend-endpoint-for-data',
    //     method: 'GET',
    //     success: function(data) {
    //         // Populate famous songs and new releases here
    //     }
    // });

    // Example data for famous songs and new releases
    var famousSongsData = ["Famous Song 1", "Famous Song 2", "Famous Song 3"];
    var newReleasesData = ["New Song 1", "New Song 2", "New Song 3"];

    var famousSongsList = $('#famousSongs');
    var newReleasesList = $('#newReleases');
    var audioPlayer = $('#audioPlayer')[0];
    var playPauseBtn = $('#playPauseBtn');

    // Populate famous songs
    famousSongsData.forEach(function(song) {
        famousSongsList.append('<li>' + song + '</li>');
    });

    // Populate new releases
    newReleasesData.forEach(function(song) {
        newReleasesList.append('<li>' + song + '</li>');
    });

    // Play/Pause button functionality
    playPauseBtn.on('click', function() {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playPauseBtn.text('Pause');
        } else {
            audioPlayer.pause();
            playPauseBtn.text('Play');
        }
    });

    // Other player control functionalities (Previous, Next) can be added similarly.
});
