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
	// Получаем элемент select с id 'importance'
	var importanceSelect = document.getElementById('importance');

	// Получаем элемент div с class 'article-container'
	var articleContainer = document.querySelector('.article-container');

	// Назначаем обработчик события изменения значения в select
	importanceSelect.addEventListener('change', function () {
		// Устанавливаем значение data-importance атрибута для div в соответствии с выбранным значением в select
		articleContainer.setAttribute('data-importance', importanceSelect.value);
	});

	// Получаем элемент первого тогла с id 'firstToggle'
	var framingToggle = document.getElementById('framing');

	// Проверяем наличие первого тогла
	if (framingToggle) {
		// Включаем первый тогл
		framingToggle.checked = false;
		// Блокируем возможность переключения первого тогла
		framingToggle.disabled = true;
	}
});
