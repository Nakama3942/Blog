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

document.addEventListener("DOMContentLoaded", function() {
	function handleButtonClick(menuId, submenuPrefixes) {
		var menu = document.getElementById(menuId);

		// Скрываем все подменю
		submenuPrefixes.forEach(function(prefix) {
			var submenu = document.getElementById(prefix + 'Menu');
			if (submenu) {
				submenu.style.display = 'none';
			}
		});

		// Переключаем состояние текущего меню
		if (menu.style.display === 'block') {
			menu.style.display = 'none';
			menu = document.getElementById(menuMap[window.location.pathname]);
			menu.style.display = 'block';
		} else {
			menu.style.display = 'block';
		}
	}

	document.getElementById('docsBtn').addEventListener('click', function() {
		handleButtonClick('docsMenu', ['blog', 'viary', 'gallery']);
		// Дополнительная логика для вложенных страниц
		if (
			window.location.pathname.startsWith('/docs')
		) {
			var blogMenu = document.getElementById('docsMenu');
			blogMenu.style.display = 'block';
		}
	});

	document.getElementById('blogBtn').addEventListener('click', function() {
		handleButtonClick('blogMenu', ['docs', 'viary', 'gallery']);
		// Дополнительная логика для вложенных страниц
		if (
			window.location.pathname.startsWith('/post_diary') ||
			window.location.pathname.startsWith('/attached_files') ||
			window.location.pathname.startsWith('/post') ||
			window.location.pathname.startsWith('/new_post') ||
			window.location.pathname.startsWith('/update_post') ||
			window.location.pathname.startsWith('/dream_diary') ||
			window.location.pathname.startsWith('/dream') ||
			window.location.pathname.startsWith('/new_dream') ||
			window.location.pathname.startsWith('/update_dream')
		) {
			var blogMenu = document.getElementById('blogMenu');
			blogMenu.style.display = 'block';
		}
	});

	document.getElementById('viaryBtn').addEventListener('click', function() {
		handleButtonClick('viaryMenu', ['docs', 'blog', 'gallery']);
		// Дополнительная логика для вложенных страниц
		if (
			window.location.pathname.startsWith('/viary')
		) {
			var viaryMenu = document.getElementById('viaryMenu');
			viaryMenu.style.display = 'block';
		}
	});

	document.getElementById('galleryBtn').addEventListener('click', function() {
		handleButtonClick('galleryMenu', ['docs', 'blog', 'viary']);
		// Дополнительная логика для вложенных страниц
		if (
			window.location.pathname.startsWith('/arts') ||
			window.location.pathname.startsWith('/screenshots') ||
			window.location.pathname.startsWith('/photos') ||
			window.location.pathname.startsWith('/codesnaps')
		) {
			var galleryMenu = document.getElementById('galleryMenu');
			galleryMenu.style.display = 'block';
		}
	});

	var menuMap = {
		'/docs': 'docsMenu',
		'/post_diary': 'blogMenu',
		'/attached_files': 'blogMenu',
		'/post': 'blogMenu',
		'/new_post': 'blogMenu',
		'/update_post': 'blogMenu',
		'/dream_diary': 'blogMenu',
		'/dream': 'blogMenu',
		'/new_dream': 'blogMenu',
		'/update_dream': 'blogMenu',
		'/viary/PL2MbnZfZV5Ku1yAsuDXz3h4bCOYDn2eJh': 'viaryMenu',
		'/arts': 'galleryMenu',
		'/screenshots': 'galleryMenu',
		'/photos': 'galleryMenu',
		'/codesnaps': 'galleryMenu'
	};

	// Получаем текущий путь
	var currentPath = window.location.pathname;
	var menuPath = Object.keys(menuMap).find(path => currentPath.startsWith(path));

	// Проверяем, если newPath это один из '/attached_files', '/post', '/new_post' или '/update_post'
	if (['/attached_files', '/post', '/new_post', '/update_post'].includes(menuPath)) {
		currentPath = '/post_diary';
	}

	if (['/dream', '/new_dream', '/update_dream'].includes(menuPath)) {
		currentPath = '/dream_diary';
	}

	// Проверяем, есть ли соответствующий id для текущего пути в объекте
	if (menuMap[currentPath]) {
		var menu = document.getElementById(menuMap[currentPath]);
		if (menu) {
			menu.style.display = 'block';
		}
	}

	if (currentPath) {
		// Удаляем класс "active" у всех ссылок
		var navLinks = document.querySelectorAll('#mainNav a');
		navLinks.forEach(function(link) {
			link.classList.remove('active');
		});

		// Добавляем класс "active" только к ссылке с соответствующим href
		var activeLink = document.querySelector(`#mainNav a[href="${currentPath}"]`);
		if (activeLink) {
			activeLink.classList.add('active');
		}
	}

	document.getElementById('emailBadge').addEventListener('click', function () {
		// Текст, который вы хотите скопировать в буфер обмена
		var textToCopy = 'nakama3942@gmail.com';

		// Помещаем текст в буфер обмена
		navigator.clipboard.writeText(textToCopy)
		.then(function () {
			// Выводим уведомление или выполните другие действия по вашему выбору
			alert('Текст скопирован в буфер обмена: ' + textToCopy);
		})
		.catch(function (err) {
			console.error('Не удалось скопировать текст: ', err);
		});
	});
});

// Скрипт для обновления версии
fetch('https://api.github.com/repos/Nakama3942/Blog/releases/latest')
.then(response => response.json())
.then(data => {
	// Извлекаем версию из ответа и обновляем элемент с id "version"
	document.getElementById('versionLink').innerText = data.tag_name;
})
.catch(error => console.error('Ошибка при получении данных:', error));
