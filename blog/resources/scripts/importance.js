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
