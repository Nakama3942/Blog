from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, send_file, jsonify
from markdown2 import markdown
from dotenv import get_key
from datetime import datetime
import os

from database import Database

# todo сделать собственное логирование (с сохранением передаваемых данных)
# todo реализовать отображение постов, какие закреплены за файлом
# todo сделать возможным отображать картинки в посте не только из resources/images, но и из files/ и arts/

app = Flask(__name__, template_folder='template', static_folder='resources')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')
app.config['POST_FOLDER'] = os.path.join(os.getcwd(), 'posts')

app.secret_key = 'your_secret_key'  # Секретный ключ для подписи сессий
ADMIN_KEY = 'admin_key'  # Ваш ключ для доступа к админским функциям

############
# Администрирование
############

# Проверка, является ли пользователь администратором
def is_admin():
	return session.get('admin', False)

# Маршрут для входа в аккаунт (с ключом)
@app.route('/login')
def login():
	key = request.args.get('key', '')
	if key == ADMIN_KEY:
		session['admin'] = True
	return redirect(url_for('diary'))

# Маршрут для выхода из аккаунта
@app.route('/logout')
def logout():
	session.pop('admin', None)
	return redirect(url_for('diary'))

############
# Открытие страниц Блога
############

@app.route('/')
def home():
	post_contents = get_posts(num_posts=5)
	return render_template('index.html', post_contents=post_contents, is_admin=is_admin())

@app.route('/autobiography')
def autobiography():
	return render_template('autobiography.html', is_admin=is_admin())

@app.route('/projects')
def projects():
	return render_template('projects.html', is_admin=is_admin())

@app.route('/documentation')
def documentation():
	return render_template('documentation.html', is_admin=is_admin())

@app.route('/diary')
def diary():
	post_contents = get_posts(num_posts=0)
	return render_template('diary.html', post_contents=post_contents, is_admin=is_admin())

@app.route('/posts/<post_title>')
def post(post_title):
	post_content = load_post_content(post_title)
	post_content['content'] = markdown(post_content['content'])
	return render_template('post.html', post_content=post_content, is_admin=is_admin())

@app.route('/viary')
def viary():
	return render_template('viary.html', api_key=get_key(".env", "YOUTUBE_API_KEY"), is_admin=is_admin())

@app.route('/dream_diary')
def dream_diary():
	return render_template('dream_diary.html', is_admin=is_admin())

@app.route('/arts')
def arts():
	return render_template('arts.html', is_admin=is_admin())

############
# Добавление постов
############

@app.route('/new_post', methods=['POST'])
def new_post():
	# Получаем список всех файлов
	with Database() as db:
		files = db.get_all_files()
	return render_template('new_post.html', files=files, is_admin=is_admin())

@app.route('/save_post', methods=['POST'])
def save_post_route():
	title = request.form['title']
	description = request.form['description']
	content = request.form['content']
	selected_file_ids = request.form.getlist('files')
	created_at = request.form.get('created_at')
	post_path = f"{os.path.join(app.config['POST_FOLDER'], title)}.md"

	# Если дата не указана - взять текущую
	if created_at:
		created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M')
	else:
		created_at = datetime.now()

	# Формируем метаданные поста
	post_metadata = {
		'description': description,
		'created_at': created_at,
		'post_path': post_path,
		'is_private': True
	}

	# Сохраняем метаданные в базе данных
	with open(post_path, 'w', encoding='utf-8') as post_file:
		post_file.write(content)
		with Database() as db:
			db.create_post(title, post_metadata)
			db.associate_files(title, selected_file_ids)

	return redirect(url_for('diary'))

@app.route('/publish_post/<post_title>', methods=['POST'])
def publish_post(post_title):
	with Database() as db:
		private_status = db.get_post(post_title).is_private
		if private_status:
			post_metadata = {
				'published_at': datetime.now(),
				'is_private': not private_status
			}
		else:
			post_metadata = {
				'published_at': None,
				'is_private': not private_status
			}
		db.update_post(post_title, post_metadata)

	return redirect(url_for('diary'))

############
# Обновление поста
############

@app.route('/update_post/<post_title>', methods=['POST'])
def update_post(post_title):
	loaded_post_content = load_post_content(post_title)
	with Database() as db:
		files = db.get_all_files()
	return render_template('update_post.html', post_content=loaded_post_content, files=files, is_admin=is_admin())

@app.route('/update_post_route/<post_title>', methods=['POST'])
def update_post_route(post_title):
	post_path = f"{os.path.join(app.config['POST_FOLDER'], post_title)}.md"

	description = request.form['description']
	selected_file_ids = request.form.getlist('files')
	content = request.form['content']

	# Формируем метаданные поста
	post_metadata = {
		'description': description,
		'last_changed_at': datetime.now()
	}

	# Сохраняем метаданные в базе данных
	with open(post_path, 'w', encoding='utf-8') as post_file:
		post_file.write(content)
		with Database() as db:
			db.update_post(post_title, post_metadata)
			db.associate_files(post_title, selected_file_ids)

	return redirect(url_for('diary'))

############
# Удаление поста
############

@app.route('/delete_post/<post_title>', methods=['POST'])
def delete_post(post_title):
	post_path = f"{os.path.join(app.config['POST_FOLDER'], post_title)}.md"
	if os.path.exists(post_path):
		with Database() as db:
			os.remove(post_path)
			db.remove_post(post_title)

	return redirect(url_for('diary'))

############
# Открытие страницы файлов
############

@app.route('/attached_files', methods=['GET', 'POST'])
def attached_files():
	with Database() as db:
		files = db.get_all_files()
	return render_template('files.html', files=files, is_admin=is_admin())

@app.route('/upload_file', methods=['POST'])
def upload_file():
	# Сохраняем файлы на сервер
	with Database() as db:
		uploaded_files = request.files.getlist('files')
		# Фильтруем файлы, чтобы оставить только те, которые не пусты
		valid_files = [file for file in uploaded_files if file.filename]
		if valid_files:
			for valid_file in valid_files:
				filename = os.path.join(app.config['UPLOAD_FOLDER'], valid_file.filename)
				valid_file.save(filename)
				db.create_file(valid_file.filename, {'type': valid_file.filename.split('.')[-1].upper()})

	return redirect(url_for('attached_files'))

@app.route('/delete_file/<filename>', methods=['DELETE'])
def delete_file(filename):
	try:
		with Database() as db:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			db.remove_file(filename)
		return jsonify({'success': True})
	except FileNotFoundError:
		return jsonify({'success': False, 'error': 'File not found'})

############
# Загрузка файлов с сервера на компьютер
############

@app.route('/files/<path:filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

############
# Функция для открытия документаций
############

@app.route('/docs/<path:subpath>/<path:filename>')
def serve_docs(subpath, filename):
	return send_file(f'N:/Blog/blog/docs/{subpath}/{filename}')

############
# Функции загрузки контента
############

def get_posts(num_posts):
	with Database() as db:
		posts = db.get_all_posts()[:num_posts] if num_posts else db.get_all_posts()
		posts_metadata = [extract_post_metadata(post_metadata) for post_metadata in posts]

	return posts_metadata

def load_post_content(title):
	with Database() as db:
		chosen_post = db.get_post(title)
		chosen_post_metadata = extract_post_metadata(chosen_post)

	# Прочитайте содержимое файла
	with open(chosen_post_metadata['post_path'], 'r', encoding='utf-8') as post_file:
		chosen_post_metadata['content'] = post_file.read()

	return chosen_post_metadata

def extract_post_metadata(post_obj):
	return {
		'title': post_obj.title,
		'description': post_obj.description,
		'files': [{'name': file.name, 'type': file.type} for file in post_obj.files],
		'created_at': post_obj.created_at.strftime('%Y-%m-%d %I:%M %p'),
		'last_changed_at': post_obj.last_changed_at.strftime('%Y-%m-%d %I:%M %p') if post_obj.last_changed_at is not None else None,
		'published_at': post_obj.published_at.strftime('%Y-%m-%d %I:%M %p') if post_obj.published_at is not None else None,
		'post_path': post_obj.post_path,
		'is_private': post_obj.is_private
	}

############
# Запуск блога
############

if __name__ == '__main__':
	app.run(debug=True)
