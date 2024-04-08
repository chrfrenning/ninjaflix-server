listVideos = function() {
    fetch('/videos')
        .then(response => response.json())
        .then(data => {
            var videoList = document.getElementById('video-list');
            videoList.children = [];

            var videos = data;
            for (var i = 0; i < videos.length; i++) {
                var video = videos[i];
                var videoItem = document.createElement('li');
                videoItem.className = 'video-list-item';
                videoList.append(videoItem);

                var videoLink = document.createElement('a');
                videoLink.href = video.watch_url;
                videoItem.append(videoLink);

                var videoThumbnail = document.createElement('img');
                videoThumbnail.src = video.thumbnail_url;
                videoThumbnail.className = "video-thumbnail";

                var videoTitle = document.createElement('div');
                videoTitle.innerText = video.title;
                videoTitle.className = "video-title";

                videoLink.append(videoThumbnail);
                videoLink.append(videoTitle);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

document.addEventListener("DOMContentLoaded", function() {
    listVideos();
});