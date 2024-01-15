// ******************************************************************************** *
// Copyright © 2023-2024 Kalynovsky Valentin. All rights reserved.                  *
//                                                                                  *
// Licensed under the Apache License, Version 2.0 (the "License");                  *
// you may not use this file except in compliance with the License.                 *
// You may obtain a copy of the License at                                          *
//                                                                                  *
//     http://www.apache.org/licenses/LICENSE-2.0                                   *
//                                                                                  *
// Unless required by applicable law or agreed to in writing, software              *
// distributed under the License is distributed on an "AS IS" BASIS,                *
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.         *
// See the License for the specific language governing permissions and              *
// limitations under the License.                                                   *
// ******************************************************************************** *

document.addEventListener("DOMContentLoaded", function () {
	// Ваш API ключ YouTube
	var apiKey = document.getElementById('videoBlog').getAttribute('youtube-api-key');

	// ID вашего плейлиста
	var playlistId = document.getElementById('videoBlog').getAttribute('playlist-id');

	// Количество видео, которые вы хотите отобразить
	var maxResults = 1000;

	// URL для запроса к YouTube Data API
	var apiUrl = 'https://www.googleapis.com/youtube/v3/playlistItems';

	// Параметры запроса
	var params = 'part=snippet&key=' + apiKey + '&playlistId=' + playlistId + '&maxResults=' + maxResults;

	// Отправка GET-запроса к YouTube Data API
	var xhr = new XMLHttpRequest();
	xhr.open('GET', apiUrl + '?' + params, true);
	xhr.onreadystatechange = function () {
		if (xhr.readyState === 4 && xhr.status === 200) {
			// Обработка данных
			var response = JSON.parse(xhr.responseText);
			if (response.items) {
				var videos = response.items;

				// Отображение видео на вашей странице
				var videoBlog = document.getElementById('videoBlog');
				videos.forEach(function (video) {
					var videoId = video.snippet.resourceId.videoId;

					// Вставка плеера в блог
					var videoPlayer = '<div class="video-container">';
					videoPlayer += '<iframe width="560" height="315" src="https://www.youtube.com/embed/' + videoId + '" frameborder="0" allowfullscreen></iframe>';
					videoPlayer += '</div>';

					videoBlog.innerHTML += videoPlayer;
				});
			} else {
				console.error('Ошибка при получении данных');
			}
		}
	};
	xhr.send();
});
