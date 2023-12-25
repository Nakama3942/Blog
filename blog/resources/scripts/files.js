document.addEventListener('DOMContentLoaded', function () {
	var modal = document.getElementById('myModal');
	var modalList = document.getElementById('postsList');
	var currentFileName;

	// Флаг, показывающий, открыто ли модальное окно
	var modalOpen = false;

	// При клике на изображение открываем модальное окно
	document.querySelectorAll('.open-modal').forEach(function (element) {
		element.addEventListener('click', function (e) {
			e.preventDefault();

			// Сохраняем имя файла
			currentFileName = this.getAttribute('file-name');

			var filePostsList = JSON.parse(this.getAttribute('file-posts-titles').replace(/'/g, '"'));
			console.log('file-posts-titles:', filePostsList);

			// Создаем список с использованием HTML-разметки
			var postLinks = filePostsList.map((post, index) => `<a href="/posts/${encodeURIComponent(post)}">${index + 1}. ${post}</a>`).join('<br>');

			// Используйте innerHTML для вставки HTML-разметки в элемент
			modalList.innerHTML = `Файл <b>${currentFileName}</b> закріплено за постами:<br>${postLinks}`;
			modal.style.display = 'block';
			modalOpen = true;
		});
	});

	// Закрываем модальное окно при клике на крестик
	document.querySelector('.close').addEventListener('click', function () {
		modal.style.display = 'none';
		modalOpen = false;
	});

	// Функция для загрузки файла
	window.downloadFile = function () {
		fetch(`/files/${encodeURIComponent(currentFileName)}`, {
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
			link.download = currentFileName;

			// Добавляем элемент в DOM и имитируем клик
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);

			// Очищаем URL-адрес Blob после скачивания
			window.URL.revokeObjectURL(link.href);
		})
		.catch(error => console.error('Ошибка:', error));
	};
});

function deleteFile(filename) {
	if (confirm(`Вы уверены, что хотите удалить файл ${filename}?`)) {
		fetch(`/delete_file/${filename}`, {
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