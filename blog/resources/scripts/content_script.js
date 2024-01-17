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

window.addEventListener('unload', function () {
	const form = document.querySelector('form');
	form.reset(); // Очищаем все поля формы
});

document.addEventListener('DOMContentLoaded', function() {
	// Вызовите вашу функцию обновления размера здесь
	auto_grow(document.getElementById('content'));

	// Отправляю запрос на сохранение контента на сервер
	const form = document.querySelector('form');
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const formData = new FormData(form);

		fetch(form.action, {
			method: 'POST',
			body: formData
		})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				// Перенаправление после успешного сохранения
				switch (form.id) {
					case 'postForm':
						window.location.href = "/post_diary";
						break;
					case 'dreamForm':
						window.location.href = "/dream_diary";
						break;
				}
			} else {
				// Если сохранение не удалось, выведите сообщение об ошибке или что-то еще
				alert('Помилка: ' + data.error_message);
			}
		})
		.catch(error => {
			alert('Невідома помилка: ' + error);
		});
	});
});

function auto_grow(element) {
	element.style.height = (element.scrollHeight) + "px";
}

function formatText(command) {
	event.preventDefault();

	const contentTextArea = document.getElementById('content');
	var selectedText = contentTextArea.value.substring(contentTextArea.selectionStart, contentTextArea.selectionEnd);

	switch (command) {
		case 'bold':
			selectedText = `**${selectedText}**`;
			break;
		case 'italic':
			selectedText = `*${selectedText}*`;
			break;
		case 'underline':
			selectedText = `<u>${selectedText}</u>`;
			break;
		case 'spoiler':
			selectedText = `<span class="spoiler">${selectedText}</span>`;
			break;
		case 'censor':
			selectedText = `<span class="censored">${selectedText}</span>`;
			break;
	}

	// Заменяем выделенный текст новым текстом
	contentTextArea.setRangeText(selectedText, contentTextArea.selectionStart, contentTextArea.selectionEnd, 'end');

	// Устанавливаем курсор в конец нового текста
    contentTextArea.focus();
    contentTextArea.setSelectionRange(contentTextArea.selectionEnd, contentTextArea.selectionEnd);
}

function insertImageTag() {
	const imageDirectorySelect = document.getElementById('image_directory');
	const imageFileNameInput = document.getElementById('image_name');
	const contentTextArea = document.getElementById('content');

	const selectedDirectory = imageDirectorySelect.value;
	const fileName = imageFileNameInput.value.trim();

	if (selectedDirectory !== '' && fileName !== '') {
		const imgTag = `<p class="image"><img src="/image/${selectedDirectory}/${fileName}" width="700px"></p>`;
		contentTextArea.value += `\n${imgTag}`;
		auto_grow(contentTextArea);
	}

	// Сброс значения селектора после добавления картинки
	imageDirectorySelect.value = '';
}

// JavaScript для отображения выбранных файлов
function handleFileSelect(event) {
	const files = event.target.files;
	const fileList = document.getElementById('fileList');

	// Обновляем список файлов
	for (const file of files) {
		const listItem = document.createElement('li');
		listItem.classList.add('file-item');

		const link = document.createElement('a');
		link.href = URL.createObjectURL(file);
		link.download = file.name;

		const icon = document.createElement('img');
		icon.src = 'resources/icons/' + getFileType(file.name) + '.png';
		icon.alt = getFileType(file.name) + ' Icon';
		icon.width = 128;
		icon.height = 128;
		icon.classList.add('file-icon');

		const fileName = document.createTextNode(file.name);

		link.appendChild(icon);
		link.appendChild(fileName);
		listItem.appendChild(link);

		fileList.appendChild(listItem);
	}
}

// Получаем тип файла по расширению
function getFileType(fileName) {
	const extension = fileName.split('.').pop().toLowerCase();
	// Ваш код определения типа файла по расширению, например, расширения 'pdf' -> 'PDF'
	return extension.toUpperCase();
}
