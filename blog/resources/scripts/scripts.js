function auto_grow(element) {
	element.style.height = "5px";
	element.style.height = (element.scrollHeight)+"px";
}

window.addEventListener('unload', function () {
	const form = document.querySelector('form');
	form.reset(); // Очищаем все поля формы
});

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