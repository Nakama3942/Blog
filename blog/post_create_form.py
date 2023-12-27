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
