# ################################################################################ #
# Copyright © 2023-2024 Kalynovsky Valentin. All rights reserved.                  #
#                                                                                  #
# Licensed under the Apache License, Version 2.0 (the "License");                  #
# you may not use this file except in compliance with the License.                 #
# You may obtain a copy of the License at                                          #
#                                                                                  #
#     http://www.apache.org/licenses/LICENSE-2.0                                   #
#                                                                                  #
# Unless required by applicable law or agreed to in writing, software              #
# distributed under the License is distributed on an "AS IS" BASIS,                #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.         #
# See the License for the specific language governing permissions and              #
# limitations under the License.                                                   #
# ################################################################################ #

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class CreatePostForm(FlaskForm):
	title = StringField('Заголовок', validators=[DataRequired()])
	description = StringField('Опис запису', validators=[DataRequired()])
	tags = StringField('Теги', validators=[DataRequired()])
	importance = SelectField(
		'Важливість',
		choices=[
			('Normal', 'Важливість: Неважливий/звичайний пост'),
			('Rare', 'Важливість: Незвичайний пост'),
			('Elite', 'Важливість: Достатньо важливий пост'),
			('Super Rare', 'Важливість: Дуже важливий пост'),
			('Ultra Rare', 'Важливість: Настають великі зміни')
		],
		default='Normal',
		validators=[DataRequired()]
	)
	created_at = DateTimeField('Дата й час написання', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
	files = SelectMultipleField('Обрані файли', coerce=int, validators=[DataRequired()])
	content = TextAreaField('Текст запису', validators=[DataRequired()])
	image_name = StringField('Назва зображення')
	image_directory = SelectField(
		'Директорія зображення',
		choices=[
			('', 'У якому сховищі зберігається зображення?'),
			('ART_FOLDER', 'Арти'),
			('SCREENSHOT_FOLDER', 'Скріншоти'),
			('PHOTO_FOLDER', 'Фотографії')
		],
		default='',
		validators=[DataRequired()]
	)
	submit = SubmitField('Зберегти пост')


class UpdatePostForm(FlaskForm):
	description = StringField('Опис запису', validators=[DataRequired()])
	tags = StringField('Теги', validators=[DataRequired()])
	importance = SelectField(
		'Важливість',
		choices=[
			('Normal', 'Важливість: Неважливий/звичайний пост'),
			('Rare', 'Важливість: Незвичайний пост'),
			('Elite', 'Важливість: Достатньо важливий пост'),
			('Super Rare', 'Важливість: Дуже важливий пост'),
			('Ultra Rare', 'Важливість: Настають великі зміни')
		],
		default='Normal',
		validators=[DataRequired()]
	)
	content = TextAreaField('Текст запису', validators=[DataRequired()])
	image_name = StringField('Назва зображення')
	image_directory = SelectField(
		'Директорія зображення',
		choices=[
			('', 'У якому сховищі зберігається зображення?'),
			('ART_FOLDER', 'Арти'),
			('SCREENSHOT_FOLDER', 'Скріншоти'),
			('PHOTO_FOLDER', 'Фотографії')
		],
		default='',
		validators=[DataRequired()]
	)
	files = SelectMultipleField('Обрані файли', coerce=int, validators=[DataRequired()])
	created_at = DateTimeField('Дата й час написання', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
	submit = SubmitField('Зберегти пост')


class CreateDreamForm(FlaskForm):
	title = StringField('Заголовок', validators=[DataRequired()])
	mood = StringField('Настрій', validators=[DataRequired()])
	tags = StringField('Теги', validators=[DataRequired()])
	importance = SelectField(
		'Якість',
		choices=[
			('Normal', 'Якість: Короткий/нудний сон'),
			('Rare', 'Якість: Простий сон'),
			('Elite', 'Якість: Достатньо цікавий сон'),
			('Super Rare', 'Якість: Дуже цікавий сон'),
			('Ultra Rare', 'Якість: Епічний тривалий сон із крутим сюжетом')
		],
		default='Normal',
		validators=[DataRequired()]
	)
	dreamed_at = DateTimeField('Час сновидіння', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
	content = TextAreaField('Сновидіння', validators=[DataRequired()])
	submit = SubmitField('Зберегти сновидіння')


class UpdateDreamForm(FlaskForm):
	mood = StringField('Настрій', validators=[DataRequired()])
	tags = StringField('Теги', validators=[DataRequired()])
	importance = SelectField(
		'Якість',
		choices=[
			('Normal', 'Якість: Короткий/нудний сон'),
			('Rare', 'Якість: Простий сон'),
			('Elite', 'Якість: Достатньо цікавий сон'),
			('Super Rare', 'Якість: Дуже цікавий сон'),
			('Ultra Rare', 'Якість: Епічний тривалий сон із крутим сюжетом')
		],
		default='Normal',
		validators=[DataRequired()]
	)
	content = TextAreaField('Сновидіння', validators=[DataRequired()])
	dreamed_at = DateTimeField('Час сновидіння', format='%Y-%m-%d %I:%M %p', validators=[DataRequired()])
	submit = SubmitField('Зберегти сновидіння')
