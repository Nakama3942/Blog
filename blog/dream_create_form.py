from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SelectMultipleField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

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
