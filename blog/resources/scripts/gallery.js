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

document.addEventListener('DOMContentLoaded', function () {
	var modal = document.getElementById('myModal');
	var modalImg = document.getElementById('img01');
	var currentImageIndex;

	var settings = document.querySelectorAll('.settings-panel');

	// Флаг, показывающий, открыто ли модальное окно
	var modalOpen = false;

	// При клике на изображение открываем модальное окно
	document.querySelectorAll('.open-modal').forEach(function (element) {
		element.addEventListener('click', function (e) {
			e.preventDefault();
			var imgSrc = this.getAttribute('data-img');
			currentImageIndex = parseInt(this.getAttribute('data-index')); // Сохраняем текущий индекс изображения
			modalImg.src = imgSrc;
			modal.style.display = 'block';
			settings[0].style.display = 'none';
			modalOpen = true;
		});
	});

	// Закрываем модальное окно при клике на крестик
	document.querySelector('.close').addEventListener('click', function () {
		modal.style.display = 'none';
		settings[0].style.display = 'block';
		modalOpen = false;
	});

	// Функция для переключения между изображениями
	window.plusSlides = function (imageIndex) {
		var images = document.querySelectorAll('.open-modal');
		var newImageIndex = currentImageIndex + imageIndex;

		if (newImageIndex >= 0 && newImageIndex < images.length) {
			currentImageIndex = newImageIndex;
			modalImg.src = images[newImageIndex].getAttribute('data-img');
		} else {
			// Показываем всплывающее сообщение
			showSnackbar(imageIndex === 1 ? 'Последнее изображение' : 'Первое изображение');
		}
	};

	// Функция для загрузки изображения
	window.downloadImage = function () {
		var image = document.querySelectorAll('.open-modal');
		var imageName = image[currentImageIndex].getAttribute('data-img');
		var folder = image[currentImageIndex].getAttribute('data-folder');

		fetch(`/image/${folder}/${encodeURIComponent(imageName.split('/').pop())}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			},
		})
		.then(response => {
			if (response.ok) {
				console.log('Серверная функция вызвана успешно');
				return response.blob();
				// Добавьте здесь код для обработки успешного вызова серверной функции
			} else {
				console.error('Ошибка при вызове серверной функции:', response.statusText);
				// Добавьте здесь код для обработки ошибки вызова серверной функции
			}
		})
		.then(blob => {
			// Создаем элемент <a> для скачивания
			var link = document.createElement('a');
			link.href = window.URL.createObjectURL(blob);
			link.download = imageName.split('/').pop();

			// Добавляем элемент в DOM и имитируем клик
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);

			// Очищаем URL-адрес Blob после скачивания
			window.URL.revokeObjectURL(link.href);
		})
		.catch(error => console.error('Ошибка:', error));
	};

	window.deleteImage = function () {
		var image = document.querySelectorAll('.open-modal');
		var imageName = image[currentImageIndex].getAttribute('data-img').split('/').pop();
		var folder = image[currentImageIndex].getAttribute('data-folder');

		if (confirm(`Вы уверены, что хотите удалить арт ${imageName}?`)) {
			fetch(`/delete_image/${folder}/${imageName}`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
				},
			})
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					// Обновить страницу или выполнить другие действия по желанию
					location.reload();
				} else {
					alert('Не удалось удалить файл.');
				}
			})
			.catch(error => console.error('Ошибка:', error));
		}
	}
});

// Функция для отображения всплывающего сообщения
function showSnackbar(message) {
	var snackbar = document.getElementById('snackbar');
	snackbar.innerText = message;
	snackbar.className = 'show';
	setTimeout(function () {
		snackbar.className = snackbar.className.replace('show', '');
	}, 3000); // Закрыть всплывающее сообщение через 3 секунды
}

function uploadFiles() {
	// Получаем инпут файла
	const imageInput = document.getElementById('imageInput');
	const images = imageInput.files;

	// Проверяем, есть ли выбранные файлы
	if (images.length === 0) {
		alert('Выберите изображения для загрузки!');
		return; // Прерываем выполнение функции, если файлы не выбраны
	}

	const formData = new FormData();
	for (let i = 0; i < images.length; i++) {
		formData.append('images', images[i]);
	}

	const sender = document.querySelector('.button-add').getAttribute('data-sender');
	const folder = document.querySelector('.button-add').getAttribute('data-folder');

	// Отправляем асинхронный запрос на сервер
	fetch(`/upload_image/${sender}/${encodeURIComponent(folder)}`, {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		// Обработка успешного ответа
		if (data.success) {
			const accessFileNames = data.access.map(access => access.filename);
			alert('Всі файли завантажено: ' + accessFileNames.join(', '));
			// Перенаправление после вывода ответа
			switch (sender) {
				case 'arts':
					window.location.href = '/arts';
					break;
				case 'screenshots':
					window.location.href = '/screenshots';
					break;
				case 'photos':
					window.location.href = '/photos';
					break;
				case 'codesnaps':
					window.location.href = '/codesnaps';
					break;
			}
		} else {
			// Обработка неудачной загрузки файлов
			for (const fail of data.fail) {
				// Обработка каждого сообщения об ошибке
				alert('Файл ' + fail.filename + ' не завантажено по причині: ' + fail.error_message);
			}
			const accessFileNames = data.access.map(access => access.filename);
			alert('Всі інші файли завантажено: ' + accessFileNames.join(', '));
			// Перенаправление после вывода ответа
			switch (sender) {
				case 'arts':
					window.location.href = '/arts';
					break;
				case 'screenshots':
					window.location.href = '/screenshots';
					break;
				case 'photos':
					window.location.href = '/photos';
					break;
				case 'codesnaps':
					window.location.href = '/codesnaps';
					break;
			}
		}
	})
	.catch(error => {
		alert('Невідома помилка: ' + error);
	});
}
