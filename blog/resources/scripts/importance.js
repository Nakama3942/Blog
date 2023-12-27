document.addEventListener("DOMContentLoaded", function() {
	var importanceElement = document.getElementById("importance");
	var importanceType = importanceElement.getAttribute('data-content-type');
	var importance = importanceElement.textContent.trim();

	if (importanceType === 'dream') {
		// Добавьте свои условия и тексты описаний для каждого значения
		var descriptions = {
			'Normal': '<i>Короткий/нудний сон</i>',
			'Rare': '<i>Простий сон</i>',
			'Elite': '<i>Достатньо цікавий сон</i>',
			'Super Rare': '<i>Дуже цікавий сон</i>',
			'Ultra Rare': '<i>Епічний тривалий сон із крутим сюжетом</i>'
		};
		// Установите текст описания в соответствии с значением importance
		importanceElement.innerHTML = descriptions[importance];
	} else if (importanceType === 'post') {
		// Добавьте свои условия и тексты описаний для каждого значения
		var descriptions = {
			'Normal': '<i>Неважливий/звичайний пост</i>',
			'Rare': '<i>Незвичайний пост</i>',
			'Elite': '<i>Достатньо важливий пост</i>',
			'Super Rare': '<i>Дуже важливий пост</i>',
			'Ultra Rare': '<i>Настають великі зміни</i>'
		};
		// Установите текст описания в соответствии с значением importance
		importanceElement.innerHTML = descriptions[importance];
	}
});