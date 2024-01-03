document.addEventListener('DOMContentLoaded', function () {
	// Получаем элемент select с id 'importance'
	var importanceSelect = document.getElementById('importance');

	// Получаем элемент div с class 'article-container'
	var articleContainer = document.querySelector('.article-container');

	// Назначаем обработчик события изменения значения в select
	importanceSelect.addEventListener('change', function () {
		// Устанавливаем значение data-importance атрибута для div в соответствии с выбранным значением в select
		articleContainer.setAttribute('data-importance', importanceSelect.value);
	});
});
