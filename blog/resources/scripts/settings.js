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
		'option1': applyFrames,
		'option2': applyThemes,
		'option3': applyMemes,
		'option4': applyStyles
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

function saveSettings(toggleId) {
	// Сохраняем текущее состояние тогла в localStorage
	var userSettings = JSON.parse(localStorage.getItem('userSettings')) || {};
	userSettings[toggleId.id] = toggleId.checked;
	localStorage.setItem('userSettings', JSON.stringify(userSettings));
}

function framing(toggleId) {
	// Включение/выключение цвета у рамочек
	console.log('Выполняем логику для Option 1. Состояние: ' + toggleId.checked);
	applyFrames(toggleId.checked);

	saveSettings(toggleId)
}

function applyFrames(isChecked) {
	// Пока не готово
}

function theming(toggleId) {
	// Переключение светлой-тёмной темы
	console.log('Выполняем логику для Option 2. Состояние: ' + toggleId.checked);
	applyThemes(toggleId.checked);

	saveSettings(toggleId)
}

function applyThemes(isChecked) {
	// Пока не готово
}

function meming(toggleId) {
	// Включение/выключение мемного режима
	console.log('Выполняем логику для Option 3. Состояние: ' + toggleId.checked);
	applyMemes(toggleId.checked);

	saveSettings(toggleId)
}

function applyMemes(isChecked) {
	// Пока не готово
}

function styling(toggleId) {
	// Включение/выключение всех стилей
	console.log('Выполняем логику для Option 4. Состояние: ' + toggleId.checked);
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
