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
		menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
	}

	document.getElementById('docsBtn').addEventListener('click', function() {
		handleButtonClick('docsMenu', ['blog', 'viary', 'gallery', 'code']);
	});

	document.getElementById('blogBtn').addEventListener('click', function() {
		handleButtonClick('blogMenu', ['docs', 'viary', 'gallery', 'code']);
		// Дополнительная логика для вложенных страниц
		if (window.location.pathname.startsWith('/diary') || window.location.pathname.startsWith('/dream_diary')) {
			var blogMenu = document.getElementById('blogMenu');
			blogMenu.style.display = 'block';
		}
	});

	document.getElementById('viaryBtn').addEventListener('click', function() {
		handleButtonClick('viaryMenu', ['docs', 'blog', 'gallery', 'code']);
		// Дополнительная логика для вложенных страниц
		if (window.location.pathname.startsWith('/viary')) {
			var viaryMenu = document.getElementById('viaryMenu');
			viaryMenu.style.display = 'block';
		}
	});

	document.getElementById('galleryBtn').addEventListener('click', function() {
		handleButtonClick('galleryMenu', ['docs', 'blog', 'viary', 'code']);
		// Дополнительная логика для вложенных страниц
		if (window.location.pathname.startsWith('/arts') || window.location.pathname.startsWith('/screenshots') || window.location.pathname.startsWith('/photos') || window.location.pathname.startsWith('/codesnaps')) {
			var galleryMenu = document.getElementById('galleryMenu');
			galleryMenu.style.display = 'block';
		}
	});

	var menuMap = {
		'/post_diary': 'blogMenu',
		'/dream_diary': 'blogMenu',
		'/viary': 'viaryMenu',
		'/arts': 'galleryMenu',
		'/screenshots': 'galleryMenu',
		'/photos': 'galleryMenu',
		'/codesnaps': 'galleryMenu'
	};

	// Получаем текущий путь
	var currentPath = window.location.pathname;

	// Проверяем, есть ли соответствующий id для текущего пути в объекте
	if (menuMap[currentPath]) {
		var menu = document.getElementById(menuMap[currentPath]);
		if (menu) {
			menu.style.display = 'block';
		}
	}

	// Получаем значение pathname из localStorage
	var activePath = localStorage.getItem('active_path');
	if (activePath) {
		// Удаляем класс "active" у всех ссылок
		var navLinks = document.querySelectorAll('#mainNav a');
		navLinks.forEach(function(link) {
			link.classList.remove('active');
		});

		// Добавляем класс "active" только к ссылке с соответствующим href
		var activeLink = document.querySelector(`#mainNav a[href="${activePath}"]`);
		if (activeLink) {
			activeLink.classList.add('active');
		}
	}

	// Добавляем обработчик событий для каждой ссылки
	var navLinks = document.querySelectorAll('#mainNav a');
	navLinks.forEach(function(link) {
		link.addEventListener('click', function() {
			// Устанавливаем значение active_path в localStorage
			var href = this.getAttribute('href');
			localStorage.setItem('active_path', href);
		});
	});
});