from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, send_file, jsonify
import markdown2
import yaml
import os
from datetime import datetime

from database import Database

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
# Отображение постов и Главная
############

@app.route('/')
def home():
	post_contents = get_posts(num_posts=5)
	return render_template('index.html', post_contents=post_contents, is_admin=is_admin())

@app.route('/diary')
def diary():
	post_contents = get_posts(num_posts=0)
	return render_template('diary.html', post_contents=post_contents, is_admin=is_admin())

def get_posts(num_posts):
	db = Database()
	posts = db.get_all_posts()[:num_posts] if num_posts else db.get_all_posts()
	db.close()
	posts.reverse()
	posts_metadata = [extract_post_metadata(post_metadata) for post_metadata in posts]
	print(posts_metadata)
	return posts_metadata

@app.route('/posts/<post_title>')
def post(post_title):
	post_content = load_post_content(post_title)
	post_content['content'] = markdown2.markdown(post_content['content'])
	return render_template('post.html', post_content=post_content, is_admin=is_admin())

def load_post_content(title):
	db = Database()
	chosen_post = db.get_post(title)
	db.close()
	chosen_post_metadata = extract_post_metadata(chosen_post)
	print(chosen_post_metadata)

	# Прочитайте содержимое файла
	with open(chosen_post_metadata['post_path'], 'r', encoding='utf-8') as post_file:
		chosen_post_metadata['content'] = post_file.read()

	return chosen_post_metadata

def extract_post_metadata(post_obj):
	return {
		'title': post_obj.title,
		'description': post_obj.description,
		'files': yaml.safe_load(post_obj.files),
		'post_datetime': post_obj.post_datetime.strftime('%Y-%m-%d %I:%M %p'),
		'post_path': post_obj.post_path,
		'is_private': post_obj.is_private
	}

############
# Добавление постов
############

@app.route('/new_post', methods=['POST'])
def new_post():
	return render_template('new_post.html', is_admin=is_admin())

@app.route('/save_post', methods=['POST'])
def save_post_route():
	title = request.form['title']
	description = request.form['description']
	files = []
	post_datetime = request.form.get('post_datetime')
	if post_datetime:
		post_datetime = datetime.strptime(post_datetime, '%Y-%m-%dT%H:%M')
	else:
		post_datetime = datetime.now()
	post_path = f"{os.path.join(app.config['POST_FOLDER'], title)}.md"
	content = request.form['content']

	is_private = request.form.get('private') == 'on'

	# Сохраняем файлы на сервер
	uploaded_files = request.files.getlist('files')
	# Фильтруем файлы, чтобы оставить только те, которые не пусты
	valid_files = [file for file in uploaded_files if file.filename]
	print(valid_files)
	if valid_files:
		for upload_file in valid_files:
			filename = os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename)
			upload_file.save(filename)
			file_metadata = {'name': upload_file.filename, 'type': upload_file.filename.split('.')[-1].upper()}
			files.append(file_metadata)

	print(files)

	# Формируем метаданные поста
	post_metadata = {
		'description': description,
		'files': str(files),
		'post_datetime': post_datetime,
		'post_path': post_path,
		'is_private': is_private
	}

	# Сохраняем метаданные в базе данных
	with open(post_path, 'w', encoding='utf-8') as post_file:
		post_file.write(content)
		db = Database()
		db.create_post(title, post_metadata)
		db.close()

	return redirect(url_for('diary'))

############
# Обновление поста
############

@app.route('/update_post/<post_title>', methods=['POST'])
def update_post(post_title):
	post_content = load_post_content(post_title)
	return render_template('update_post.html', post_content=post_content, is_admin=is_admin())

@app.route('/update_post_route/<post_title>', methods=['POST'])
def update_post_route(post_title):
	post_path = f"{os.path.join(app.config['POST_FOLDER'], post_title)}.md"

	description = request.form['description']
	content = request.form['content']
	is_private = request.form.get('private') == 'on'

	# Формируем метаданные поста
	post_metadata = {
		'description': description,
		'is_private': is_private
	}

	# Сохраняем метаданные в базе данных
	with open(post_path, 'w', encoding='utf-8') as post_file:
		post_file.write(content)
		db = Database()
		db.update_post(post_title, post_metadata)
		db.close()

	return redirect(url_for('diary'))

############
# Удаление поста
############

@app.route('/delete_post/<post_title>', methods=['POST'])
def delete_post(post_title):
	post_path = f"{os.path.join(app.config['POST_FOLDER'], post_title)}.md"
	if os.path.exists(post_path):
		db = Database()
		post_files = yaml.safe_load(db.get_post(post_title).files)
		for post_file in post_files:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post_file['name']))
		db.remove_post(post_title)
		db.close()
		os.remove(post_path)

	return redirect(url_for('diary'))

############
# Открытие страницы файлов
############

@app.route('/attached_files', methods=['GET', 'POST'])
def attached_files():
	db = Database()
	files = db.get_all_files()
	db.close()
	return render_template('files.html', files=files, is_admin=is_admin())

@app.route('/upload_file', methods=['POST'])
def upload_file():
	# Сохраняем файлы на сервер
	db = Database()
	uploaded_files = request.files.getlist('files')
	print(uploaded_files)
	# Фильтруем файлы, чтобы оставить только те, которые не пусты
	valid_files = [file for file in uploaded_files if file.filename]
	if valid_files:
		for valid_file in valid_files:
			filename = os.path.join(app.config['UPLOAD_FOLDER'], valid_file.filename)
			valid_file.save(filename)
			db.create_file(valid_file.filename, {'type': valid_file.filename.split('.')[-1].upper()})

	db.close()
	return redirect(url_for('attached_files'))

@app.route('/delete_file/<filename>', methods=['DELETE'])
def delete_file(filename):
	try:
		db = Database()
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		db.remove_file(filename)
		db.close()
		return jsonify({'success': True})
	except:
		return jsonify({'success': False})

############
# Загрузка файлов с сервера на компьютер
############

@app.route('/files/<path:filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

############
# Остальные странички
############

@app.route('/autobiography')
def autobiography():
	return render_template('autobiography.html', is_admin=is_admin())

@app.route('/projects')
def projects():
	return render_template('projects.html', is_admin=is_admin())

@app.route('/documentation')
def documentation():
	return render_template('documentation.html', is_admin=is_admin())

@app.route('/viary')
def viary():
	return render_template('viary.html', is_admin=is_admin())

@app.route('/dream_diary')
def dream_diary():
	return render_template('dream_diary.html', is_admin=is_admin())

@app.route('/arts')
def arts():
	return render_template('arts.html', is_admin=is_admin())

############
# Функция для открытия документаций
############

@app.route('/docs/<path:subpath>/<path:filename>')
def serve_docs(subpath, filename):
	return send_file(f'N:/Blog/blog/docs/{subpath}/{filename}')

############
# Запуск блога
############

if __name__ == '__main__':
	app.run(debug=True)
