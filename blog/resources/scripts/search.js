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
	const searchInput = document.getElementById('searchInput');
	const searchScope = document.getElementById('searchScope');
	const searchResultsModal = document.getElementById('searchResultsModal');
	const searchResultsContainer = document.getElementById('searchResultsContainer');

	// Получаем значение атрибута data-page
	const pageType = document.querySelector('script[data-page]').getAttribute('data-page');

	let timeoutId;

	// Очищаем содержимое поля ввода при обновлении страницы
	window.addEventListener('beforeunload', function () {
		searchInput.value = '';
		hideSearchResults();
	});

	// Обработчик события для изменения колонки поиска
	searchScope.addEventListener('change', function () {
		const query = searchInput.value;
		const scope = searchScope.value;
		searchOnServer(query, scope);
	});

	// Обработчик ввода
	searchInput.addEventListener('input', function () {
		handleInputChange();
	});

	function handleInputChange() {
		clearTimeout(timeoutId);

		// Устанавливаем таймер, чтобы не отправлять запросы слишком часто
		timeoutId = setTimeout(function () {
			const query = searchInput.value;
			const scope = searchScope.value;

			// Отправляем запрос на сервер
			searchOnServer(query, scope);
		}, 300);
	}

	// Обработчики событий для показа/скрытия модального окна при фокусе на поле ввода
	searchInput.addEventListener('focus', function () {
		showSearchResults();
	});
	searchInput.addEventListener('blur', function () {
		// Проверяем, была ли нажата ссылка
		if (event.relatedTarget && event.relatedTarget.tagName === 'A') {
			return;
		}

		// Если не была нажата ссылка, скрываем модальное окно
		hideSearchResults();
	});
	searchScope.addEventListener('focus', function () {
		showSearchResults();
	});
	searchScope.addEventListener('blur', function () {
		// Проверяем, была ли нажата ссылка
		if (event.relatedTarget && event.relatedTarget.tagName === 'A') {
			return;
		}

		// Если не была нажата ссылка, скрываем модальное окно
		hideSearchResults();
	});

	// Функция для отправки запроса на сервер
	function searchOnServer(query, scope) {
		const column = scope.toLowerCase();  // Приводим к нижнему регистру, чтобы соответствовать названию колонки
		let url;

		switch (pageType) {
			case 'Posts':
				url = `/search_post?column=${column}&text=${query}`;
				break;
			case 'Dreams':
				url = `/search_dream?column=${column}&text=${query}`;
				break;
		}

		console.log('Отправка запроса на сервер');

		fetch(url)
			.then(response => response.json())
			.then(data => {
				if (data.success) {
					// Обновляем результаты на странице
					console.log(data.results);
					updateSearchResults(data.results);
				} else {
					console.error('Ошибка при выполнении запроса:', data.error_message);
				}
			})
			.catch(error => console.error('Ошибка при выполнении запроса:', error));
	}

	// Функция для обновления результатов поиска на странице
	function updateSearchResults(results) {
		// Очищаем содержимое контейнера
		searchResultsContainer.innerHTML = '';

		// Перебираем результаты поиска и создаем HTML-элементы для каждого поста
		results.forEach(postMetadata => {
			const article = document.createElement('article');

			const titleLink = document.createElement('a');
			titleLink.href = `/post/${encodeURIComponent(postMetadata.title)}`;

			const title = document.createElement('h2');
			title.textContent = postMetadata.title;
			titleLink.appendChild(title);

			const description = document.createElement('p');
			description.textContent = postMetadata.description;

			const tagsParagraph = document.createElement('p');
			tagsParagraph.textContent = `Теги: ${postMetadata.tags.join(', ')}`;

			// Добавляем созданные элементы к родительскому элементу
			article.appendChild(titleLink);
			article.appendChild(description);
			article.appendChild(tagsParagraph);
			searchResultsContainer.appendChild(article);
		});

		// Показываем модальное окно
		showSearchResults();
	}

	// Функция для показа модального окна результатов поиска
	function showSearchResults() {
		if (searchResultsModal) {
			searchResultsModal.style.display = searchResultsContainer.children.length > 0 ? 'block' : 'none';
		}
	}

	// Функция для скрытия модального окна результатов поиска
	function hideSearchResults() {
		if (searchResultsModal) {
			searchResultsModal.style.display = 'none';
		}
	}
});
