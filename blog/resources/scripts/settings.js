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

//Устанавливаю настройки при первой загрузке сайта
function onPageLoad() {
	// Проверяем, была ли функция уже вызвана
	if (!localStorage.getItem('pageLoaded')) {
		// Ваш код здесь
		styling(document.getElementById('styling'));
		meming(document.getElementById('meming'));
		theming(document.getElementById('theming'));
		framing(document.getElementById('framing'));

		// Помечаем, что функция была вызвана
		localStorage.setItem('pageLoaded', true);
	}
}
window.onload = onPageLoad;

document.addEventListener('DOMContentLoaded', function () {
	var toggleWrappers = document.querySelectorAll('.toggle-wrapper');

	toggleWrappers.forEach(function (wrapper) {
		var toggleColor = wrapper.getAttribute('toggle-color');
		if (toggleColor) {
			wrapper.style.setProperty('--toggle-color', toggleColor);
		}
	});

	// Проверяем, сохранены ли настройки в localStorage
	var savedSettings = localStorage.getItem('userSettings');
	if (savedSettings) {
		// Если настройки сохранены, применяем их
		var settings = JSON.parse(savedSettings)
		for (var toggleId in settings) {
			if (settings.hasOwnProperty(toggleId)) {
				var toggle = document.getElementById(toggleId);
				if (toggle) {
					toggle.checked = settings[toggle.id];
				}
			}
		}
		applySettings();
	}
});

function applySettings() {
	// Получаем все тоглы на странице
	var allToggles = document.querySelectorAll('.toggle');

	// Создаем объект с соответствиями идентификаторов и функций
	var toggleFunctions = {
		'styling': applyStyles,
		'meming': applyMemes,
		'theming': applyThemes,
		'framing': applyFrames
	};

	// Проходимся по каждому тоглу и вызываем соответствующую функцию
	allToggles.forEach(function (toggle) {
		var toggleId = toggle.id;
		var toggleFunction = toggleFunctions[toggleId];

		if (toggleFunction) {
			toggleFunction(toggle.checked);
		}
	});
}

function styling(toggleId) {
	// Включение/выключение всех стилей
	applyStyles(toggleId.checked);

	saveSettings(toggleId)
}

function applyStyles(isChecked) {
	// Получаем все теги link с подключенными стилями
	var styleLinks = document.querySelectorAll('link[rel="stylesheet"]');

	// Включаем/выключаем стили, удаляя или добавляя элементы
	styleLinks.forEach(function (link) {
		link.disabled = !isChecked;
	});
}

function meming(toggleId) {
	// Включение/выключение мемного режима
	applyMemes(toggleId.checked);

	saveSettings(toggleId)
}

function applyMemes(isChecked) {
	//
	var memeArticle = document.querySelectorAll('.article-container');
	// Получаем все теги, содержащие атрибут meme и not-meme
	var memeElements = document.querySelectorAll('[meme]');
	var notMemeElements = document.querySelectorAll('[not-meme]');

	memeArticle.forEach(function (element) {
		if (isChecked){
			element.setAttribute('meme-article', '');
		} else {
			element.removeAttribute('meme-article');
		}
	});

	// Включаем/выключаем отображение элементов с атрибутом meme
	memeElements.forEach(function (element) {
		element.style.display = isChecked ? 'block' : 'none';
	});

	notMemeElements.forEach(function (element) {
		element.style.display = isChecked ? 'none' : 'block';
	});
}

function theming(toggleId) {
	// Переключение светлой-тёмной темы
	applyThemes(toggleId.checked);

	saveSettings(toggleId)
}

function applyThemes(isChecked) {
	const links = document.querySelectorAll('link[rel="stylesheet"]');

	if (isChecked) {
		links.forEach(link => {
			let href = link.getAttribute('href');
			href = href.replace('/light/', '/night/');

			// Добавляем темный стиль, не удаляя светлый
			if (href.includes('/night/')) {
				link.insertAdjacentHTML('afterend', `<link href="${href}" rel="stylesheet">`);
			}
		});
	} else {
		// Удаляем все темные стили
		links.forEach(link => {
			const href = link.getAttribute('href');

			// Добавляем темный стиль, не удаляя светлый
			if (href.includes('/night/')) {
				link.remove();
			}
		});
	}
}

function framing(toggleId) {
	// Включение/выключение цвета у рамочек
	applyFrames(toggleId.checked);

	saveSettings(toggleId)
}

function applyFrames(isChecked) {
	var articleContainers = document.querySelectorAll('.article-container');

	articleContainers.forEach(function (container) {
		if (isChecked) {
			container.setAttribute('temp-data-importance', container.getAttribute('data-importance') || 'Normal');
			container.setAttribute('data-importance', 'Normal');
		} else {
			container.setAttribute('data-importance', container.getAttribute('temp-data-importance') || container.getAttribute('data-importance'));
			container.removeAttribute('temp-data-importance');
		}
	});
}

function saveSettings(toggleId) {
	// Сохраняем текущее состояние тогла в localStorage
	var userSettings = JSON.parse(localStorage.getItem('userSettings')) || {};
	userSettings[toggleId.id] = toggleId.checked;
	localStorage.setItem('userSettings', JSON.stringify(userSettings));
}
