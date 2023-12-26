from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, send_file, jsonify
from markdown2 import markdown
from dotenv import get_key
from PIL import Image
from datetime import datetime
import os

from database import Database

# todo реализовать дневник сновидений
# todo добавить больше плейлистов в видеодневник
# todo добавить страницы для хранения фрагментов кода
# todo сделать возможность указать настроение в посте, которое будет выражаться изменением рамочки поста (и для сна тоже)
# todo добавить теги к постам и сновидениям
# todo запретить создавать посты с одинаковыми названиями и проверять файлы на названия; если файл уже загружен - не грузить его и предупредить меня
# todo добавить поиск в постах и сновидениях по словам в названии, тексте, и поиск по тегам
# todo заменить select2 на что-то другое
# todo перенести кнопку удаления файла/изображения в модальное окно
# todo сделать анимацию открывания вложенных вкладок во вкладках в навигационной панели

# todo после завершения разработки адаптировать дизайн под телефоны

app = Flask(__name__, template_folder='template', static_folder='resources')
app.config['POST_FOLDER'] = os.path.join(os.getcwd(), 'posts')
app.config['FILE_FOLDER'] = os.path.join(os.getcwd(), 'files')
app.config['DREAM_FOLDER'] = os.path.join(os.getcwd(), 'dreams')
app.config['ART_FOLDER'] = os.path.join(os.getcwd(), 'gallery/arts')
app.config['THUMBNAIL_ART_FOLDER'] = os.path.join(os.getcwd(), 'gallery/arts/thumbnails')
app.config['SCREENSHOT_FOLDER'] = os.path.join(os.getcwd(), 'gallery/screenshots')
app.config['THUMBNAIL_SCREENSHOT_FOLDER'] = os.path.join(os.getcwd(), 'gallery/screenshots/thumbnails')
app.config['PHOTO_FOLDER'] = os.path.join(os.getcwd(), 'gallery/photos')
app.config['THUMBNAIL_PHOTO_FOLDER'] = os.path.join(os.getcwd(), 'gallery/photos/thumbnails')

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
	return render_template(
		'index.html',
		active_tab='',
		post_contents=post_contents,
		is_admin=is_admin()
	)

@app.route('/autobiography')
def autobiography():
	return render_template(
		'autobiography.html',
		active_tab='autobiography',
		is_admin=is_admin()
	)

@app.route('/projects')
def projects():
	return render_template(
		'projects.html',
		active_tab='projects',
		is_admin=is_admin()
	)

@app.route('/diary')
def diary():
	post_contents = get_posts(num_posts=0)
	return render_template(
		'diary.html',
		active_tab='diary',
		post_contents=post_contents,
		is_admin=is_admin()
	)

@app.route('/posts/<post_title>')
def post(post_title):
	post_content = load_post_content(post_title)
	post_content['content'] = markdown(post_content['content'])
	return render_template(
		'post.html',
		active_tab='post',
		post_content=post_content,
		is_admin=is_admin()
	)

@app.route('/viary')
def viary():
	return render_template(
		'viary.html',
		active_tab='viary',
		youtube_api_key=get_key(".env", "YOUTUBE_API_KEY"),
		playlist_id=get_key(".env", "PLAYLIST_ID"),
		is_admin=is_admin()
	)

@app.route('/dream_diary')
def dream_diary():
	return render_template(
		'dream_diary.html',
		active_tab='dream_diary',
		is_admin=is_admin()
	)

@app.route('/arts')
def arts():
	with Database() as db:
		db_arts = db.get_all_arts()
	return render_template(
		'gallery.html',
		active_tab='arts',
		page_data={ 'title': 'Арти', 'sender': 'arts', 'folder': 'ART_FOLDER' },
		images=db_arts,
		is_admin=is_admin()
	)

@app.route('/screenshots')
def screenshots():
	with Database() as db:
		db_screenshots = db.get_all_screenshots()
	return render_template(
		'gallery.html',
		active_tab='screenshots',
		page_data={ 'title': 'Скріни', 'sender': 'screenshots', 'folder': 'SCREENSHOT_FOLDER' },
		images=db_screenshots,
		is_admin=is_admin()
	)

@app.route('/photos')
def photos():
	with Database() as db:
		db_photos = db.get_all_photos()
	return render_template(
		'gallery.html',
		active_tab='photos',
		page_data={ 'title': 'Фотографії', 'sender': 'photos', 'folder': 'PHOTO_FOLDER' },
		images=db_photos,
		is_admin=is_admin()
	)

@app.route('/gists')
def gists():
	return render_template(
		'gist.html',
		active_tab='gists',
		is_admin=is_admin()
	)

@app.route('/codesnaps')
def codesnaps():
	return render_template(
		'codesnap.html',
		active_tab='codesnaps',
		is_admin=is_admin()
	)

############
# Работа с постами
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
	with open(post_path, 'w', encoding='utf-8', newline='') as post_file:
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
	with open(post_path, 'w', encoding='utf-8', newline='') as post_file:
		post_file.write(content)
		with Database() as db:
			db.update_post(post_title, post_metadata)
			db.associate_files(post_title, selected_file_ids)

	return redirect(url_for('diary'))

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
		files_data = [
			{
				'name': file.name,
				'type': file.type,
				'posts_titles': [post_data.title for post_data in file.posts]
			} for file in files
		]
	return render_template('files.html', files=files_data, is_admin=is_admin())

@app.route('/upload_file', methods=['POST'])
def upload_file():
	# Сохраняем файлы на сервер
	with Database() as db:
		uploaded_files = request.files.getlist('files')
		# Фильтруем файлы, чтобы оставить только те, которые не пусты
		valid_files = [file for file in uploaded_files if file.filename]
		if valid_files:
			for valid_file in valid_files:
				filename = os.path.join(app.config['FILE_FOLDER'], valid_file.filename)
				valid_file.save(filename)
				db.create_file(valid_file.filename, {'type': valid_file.filename.split('.')[-1].upper()})

	return redirect(url_for('attached_files'))

@app.route('/delete_file/<filename>', methods=['DELETE'])
def delete_file(filename):
	try:
		with Database() as db:
			os.remove(os.path.join(app.config['FILE_FOLDER'], filename))
			db.remove_file(filename)
		return jsonify({'success': True})
	except FileNotFoundError:
		return jsonify({'success': False, 'error': 'File not found'})

############
# Открытие страницы сновидений
############

############
# Страница галереи
############

@app.route('/image/<folder>/<filename>')
def image(folder, filename):
	return send_from_directory(app.config[folder], filename)

@app.route('/upload_image/<sender>/<folder>', methods=['POST'])
def upload_image(sender, folder):
	# Сохраняем файлы на сервер
	with Database() as db:
		uploaded_images = request.files.getlist('images')
		# Фильтруем изображения, чтобы оставить только те, которые не пусты
		valid_images = [uploaded_image for uploaded_image in uploaded_images if uploaded_image.filename]
		if valid_images:
			for valid_image in valid_images:
				filename = os.path.join(app.config[folder], valid_image.filename)
				valid_image.save(filename)
				match sender:
					case 'arts':
						db.create_art(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})
					case 'screenshots':
						db.create_screenshot(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})
					case 'photos':
						db.create_photo(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})

				# Открываем изображение
				original_image = Image.open(filename)

				# Создаем миниатюру с максимальным размером 128x128
				image_thumbnail = original_image.copy()
				image_thumbnail.thumbnail((128, 128))

				# Сохраняем миниатюру в директорию thumbnail
				image_thumbnail.save(os.path.join(app.config[f'THUMBNAIL_{folder}'], valid_image.filename))

	return redirect(url_for(sender))

@app.route('/delete_image/<folder>/<filename>', methods=['DELETE'])
def delete_image(folder, filename):
	try:
		with Database() as db:
			os.remove(os.path.join(app.config[folder], filename))
			os.remove(os.path.join(app.config[f'THUMBNAIL_{folder}'], filename))
			match folder:
				case 'ART_FOLDER':
					db.remove_art(filename)
				case 'SCREENSHOT_FOLDER':
					db.remove_screenshot(filename)
				case 'PHOTO_FOLDER':
					db.remove_photo(filename)
		return jsonify({'success': True})
	except FileNotFoundError:
		return jsonify({'success': False, 'error': 'Art not found'})

############
# Загрузка файлов с сервера на компьютер
############

@app.route('/files/<path:filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['FILE_FOLDER'], filename)

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
