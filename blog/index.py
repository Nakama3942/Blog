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

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, send_file, jsonify, make_response
from markdown2 import markdown
from dotenv import get_key
from PIL import Image
from datetime import datetime
import os

from database import Database
from forms import CreatePostForm, UpdatePostForm, CreateDreamForm, UpdateDreamForm

# Возможна оптимизация: если будут проблемы с загрузкой большого количества контента - нужно
#  просто реализовать подгрузку данных из БД.

# Завершение проекта
# todo - после завершения разработки адаптировать дизайн под телефоны
# todo - сделать тёмную тему

app = Flask(__name__, template_folder='template', static_folder='resources')
app.config['CONTENT_FOLDER'] = os.path.join(os.getcwd(), 'content')
app.config['POST_FOLDER'] = os.path.join(os.getcwd(), 'content/posts')
app.config['FILE_FOLDER'] = os.path.join(os.getcwd(), 'content/files')
app.config['DREAM_FOLDER'] = os.path.join(os.getcwd(), 'content/dreams')
app.config['ART_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/arts')
app.config['THUMBNAIL_ART_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/arts/thumbnails')
app.config['SCREENSHOT_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/screenshots')
app.config['THUMBNAIL_SCREENSHOT_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/screenshots/thumbnails')
app.config['PHOTO_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/photos')
app.config['THUMBNAIL_PHOTO_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/photos/thumbnails')
app.config['CODESNAPS_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/codesnaps')
app.config['THUMBNAIL_CODESNAPS_FOLDER'] = os.path.join(os.getcwd(), 'content/gallery/codesnaps/thumbnails')

############
# Администрирование
############

app.secret_key = get_key(".env", "SECRET_KEY")  # Секретный ключ для подписи сессий

# Проверка, является ли пользователь администратором
def is_admin():
	return session.get('admin', False)

# Маршрут для входа в аккаунт (с ключом)
@app.route('/login')
def login():
	key = request.args.get('key', '')
	if key == get_key(".env", "ADMIN_KEY"):
		session['admin'] = True
	return redirect(url_for('home'))

# Маршрут для выхода из аккаунта
@app.route('/logout')
def logout():
	session.pop('admin', None)
	return redirect(url_for('home'))

############
# Открытие страниц Блога
############

@app.route('/')
def home():
	return render_template(
		'index.html',
		active_tab='',
		index_content=markdown(get_content('index')),
		posts_content=get_posts(5),
		dreams_content=get_dreams(5),
		is_admin=is_admin()
	)

@app.route('/autobiography')
def autobiography():
	return render_template(
		'biography.html',
		biography_content=markdown(get_content('biography')),
		active_tab='autobiography',
		is_admin=is_admin()
	)

@app.route('/projects')
def projects():
	projects_data_list = get_content('projects').replace('\n', '').split('* ')
	projects_content = [
		{
			'type': projects_data_list[i],
			'link': projects_data_list[i + 1],
			'name': projects_data_list[i + 2],
			'desc': projects_data_list[i + 3],
			'time': projects_data_list[i + 4]
		}
		for i in range(1, len(projects_data_list), 5)
	]

	return render_template(
		'projects.html',
		projects_content=projects_content,
		active_tab='projects',
		is_admin=is_admin()
	)

@app.route('/post_diary')
def post_diary():
	posts_content = get_posts(0)
	return render_template(
		'post_diary.html',
		active_tab='post_diary',
		posts_content=posts_content,
		is_admin=is_admin()
	)

@app.route('/post/<post_title>')
def post(post_title):
	post_content = load_post_content(post_title)
	post_content['content'] = markdown(post_content['content'])
	return render_template(
		'post.html',
		active_tab='post',
		post_content=post_content,
		is_admin=is_admin()
	)

@app.route('/dream_diary')
def dream_diary():
	dreams_content = get_dreams(0)
	return render_template(
		'dream_diary.html',
		active_tab='dream_diary',
		dreams_content=dreams_content,
		is_admin=is_admin()
	)

@app.route('/dream/<dream_title>')
def dream(dream_title):
	dream_content = load_dream_content(dream_title)
	dream_content['content'] = markdown(dream_content['content'])
	return render_template(
		'dream.html',
		active_tab='dream',
		dream_content=dream_content,
		is_admin=is_admin()
	)

@app.route('/viary/<playlist_id>')
def viary(playlist_id):
	return render_template(
		'viary.html',
		active_tab='viary',
		youtube_api_key=get_key(".env", "YOUTUBE_API_KEY"),
		playlist_id=playlist_id,
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

@app.route('/codesnaps')
def codesnaps():
	with Database() as db:
		db_codesnaps = db.get_all_codesnaps()
	return render_template(
		'gallery.html',
		active_tab='photos',
		page_data={'title': 'CodeSnaps', 'sender': 'codesnaps', 'folder': 'CODESNAPS_FOLDER'},
		images=db_codesnaps,
		is_admin=is_admin()
	)

############
# Работа с постами
############

@app.route('/new_post')
def new_post():
	form = CreatePostForm()
	with Database() as db:
		files = db.get_all_files()  # Получаем список всех файлов

	form.files.choices = [(file.id, file.name) for file in files]

	return render_template('post_new.html', form=form, is_admin=is_admin())

@app.route('/save_post', methods=['POST'])
def save_post_route():
	title = request.form['title']
	with Database() as db:
		if not db.check_post(title):
			return jsonify({'success': False, 'error_message': 'Пост із такою назвою вже існує'})
	description = request.form['description']
	tags = request.form['tags']
	importance = request.form['importance']
	created_at = request.form.get('created_at')
	selected_file_ids = request.form.getlist('files')
	content = request.form['content']

	# Якщо дату написання не зазначено - взяти поточну
	if created_at:
		created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M')
	else:
		created_at = datetime.now()

	# Формуємо метаданні посту
	post_metadata = {
		'description': description,
		'tags': tags,
		'importance': importance,
		'created_at': created_at,
		'published_at': datetime.now()
	}

	# Зберігаємо метадані в БД
	with open(f"{os.path.join(app.config['POST_FOLDER'], title)}.md", 'w', encoding='utf-8', newline='') as post_file:
		post_file.write(content)
		with Database() as db:
			db.create_post(title, post_metadata)
			db.associate_files(title, selected_file_ids)

	return jsonify({'success': True})

@app.route('/update_post/<post_title>')
def update_post(post_title):
	form = UpdatePostForm()
	with Database() as db:
		files = db.get_all_files()  # Получаем список всех файлов

	form.files.choices = [(file.id, file.name) for file in files]

	loaded_post_content = load_post_content(post_title)

	# Устанавливаем значения по умолчанию для поля files
	form.description.default = loaded_post_content.pop('description')
	form.tags.default = ', '.join(loaded_post_content.pop('tags'))
	form.importance.default = loaded_post_content.pop('importance')
	loaded_post_content['created_at'] = datetime.strptime(datetime.strptime(loaded_post_content['created_at'], '%Y-%m-%d %I:%M %p').strftime('%Y-%m-%dT%H:%M'), '%Y-%m-%dT%H:%M')
	form.files.default = [file['id'] for file in loaded_post_content.pop('files')]
	form.content.default = loaded_post_content.pop('content')
	form.process()

	return render_template('post_update.html', form=form, post_content=loaded_post_content, is_admin=is_admin())

@app.route('/update_post_route/<post_title>', methods=['POST'])
def update_post_route(post_title):
	description = request.form['description']
	tags = request.form['tags']
	importance = request.form['importance']
	created_at = datetime.strptime(request.form.get('created_at'), '%Y-%m-%dT%H:%M')
	selected_file_ids = request.form.getlist('files')
	content = request.form['content']

	# Формируем метаданные поста
	post_metadata = {
		'description': description,
		'tags': tags,
		'importance': importance,
		'created_at': created_at,
		'last_changed_at': datetime.now()
	}

	# Сохраняем метаданные в базе данных
	with open(f"{os.path.join(app.config['POST_FOLDER'], post_title)}.md", 'w', encoding='utf-8', newline='') as post_file:
		post_file.write(content)
		with Database() as db:
			if db.get_post(post_title).created_at.replace(second=0, microsecond=0) == post_metadata['created_at']:
				post_metadata.pop('created_at')
			db.update_post(post_title, post_metadata)
			db.associate_files(post_title, selected_file_ids)

	return jsonify({'success': True})

@app.route('/delete_post/<post_title>')
def delete_post(post_title):
	with Database() as db:
		post_path = f"{os.path.join(app.config['POST_FOLDER'], post_title)}.md"
		if os.path.exists(post_path):
			os.remove(post_path)
			db.remove_post(post_title)

	return redirect(url_for('post_diary'))

@app.route('/search_post', methods=['GET'])
def search_post():
	try:
		# Получаем параметры запроса от клиента
		column = request.args.get('column')
		text = request.args.get('text')

		# Вызываем метод поиска в базе данных
		with Database() as db:
			search_result = db.search_post(column, text)
			search_result_metadata = [extract_post_metadata(post_metadata) for post_metadata in search_result]

		# Возвращаем результаты в формате JSON
		return jsonify({'success': True, 'results': search_result_metadata})
	except Exception as e:
		return jsonify({'success': False, 'error_message': str(e)})

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
	access_responses = []
	fail_responses = []

	with Database() as db:
		uploaded_files = request.files.getlist('files')
		# Фильтруем файлы, чтобы оставить только те, которые не пусты
		valid_files = [file for file in uploaded_files if file.filename]
		if valid_files:
			for valid_file in valid_files:
				if db.check_file(valid_file.filename):
					db.create_file(valid_file.filename, {'type': valid_file.filename.split('.')[-1].upper()})
					access_responses.append({'filename': valid_file.filename})
				else:
					fail_responses.append({'filename': valid_file.filename, 'error_message': 'Файл із такою назвою вже існує на сервері'})
					continue

				valid_file.save(os.path.join(app.config['FILE_FOLDER'], valid_file.filename))

	# Используем генератор для возврата ответов
	if len(fail_responses) == 0:
		# Если есть хотя бы одна успешная загрузка, вернем общий успех
		return jsonify({'success': True, 'access': access_responses})
	else:
		# Вернем все неуспешные загрузки
		return jsonify({'success': False, 'fail': fail_responses, 'access': access_responses})

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

@app.route('/new_dream')
def new_dream():
	form = CreateDreamForm()
	return render_template('dream_new.html', form=form, is_admin=is_admin())

@app.route('/save_dream', methods=['POST'])
def save_dream_route():
	title = request.form['title']
	with Database() as db:
		if not db.check_dream(title):
			return jsonify({'success': False, 'error_message': 'Сновидіння із такою назвою вже існує'})
	mood = request.form['mood']
	tags = request.form['tags']
	importance = request.form['importance']
	dreamed_at = datetime.strptime(request.form.get('dreamed_at'), '%Y-%m-%dT%H:%M')
	dream_content = request.form['content']

	# Формируем метаданные поста
	dream_metadata = {
		'mood': mood,
		'tags': tags,
		'importance': importance,
		'dreamed_at': dreamed_at,
		'published_at': datetime.now()
	}

	# Сохраняем метаданные в базе данных
	with open(f"{os.path.join(app.config['DREAM_FOLDER'], title)}.md", 'w', encoding='utf-8', newline='') as dream_file:
		with Database() as db:
			dream_file.write(dream_content)
			db.create_dream(title, dream_metadata)

	return jsonify({'success': True})

@app.route('/update_dream/<dream_title>')
def update_dream(dream_title):
	form = UpdateDreamForm()

	dream_content = load_dream_content(dream_title)

	# Устанавливаем значения по умолчанию для поля files
	form.mood.default = dream_content.pop('mood')
	form.tags.default = ', '.join(dream_content.pop('tags'))
	form.importance.default = dream_content.pop('importance')
	dream_content['dreamed_at'] = datetime.strptime(datetime.strptime(dream_content['dreamed_at'], '%Y-%m-%d %I:%M %p').strftime('%Y-%m-%dT%H:%M'), '%Y-%m-%dT%H:%M')
	form.content.default = dream_content.pop('content')
	form.process()

	return render_template('dream_update.html', form=form, dream_content=dream_content, is_admin=is_admin())

@app.route('/update_dream_route/<dream_title>', methods=['POST'])
def update_dream_route(dream_title):
	mood = request.form['mood']
	tags = request.form['tags']
	importance = request.form['importance']
	dreamed_at = datetime.strptime(request.form['dreamed_at'], '%Y-%m-%dT%H:%M')
	content = request.form['content']

	# Формируем метаданные поста
	post_metadata = {
		'mood': mood,
		'tags': tags,
		'importance': importance,
		'dreamed_at': dreamed_at
	}

	# Сохраняем метаданные в базе данных
	with open(f"{os.path.join(app.config['DREAM_FOLDER'], dream_title)}.md", 'w', encoding='utf-8', newline='') as dream_file:
		dream_file.write(content)
		with Database() as db:
			db.update_dream(dream_title, post_metadata)

	return jsonify({'success': True})

@app.route('/delete_dream/<dream_title>')
def delete_dream(dream_title):
	with Database() as db:
		dream_path = f"{os.path.join(app.config['DREAM_FOLDER'], dream_title)}.md"
		if os.path.exists(dream_path):
			os.remove(dream_path)
			db.remove_dream(dream_title)

	return redirect(url_for('dream_diary'))

@app.route('/search_dream', methods=['GET'])
def search_dream():
	try:
		# Получаем параметры запроса от клиента
		column = request.args.get('column')
		text = request.args.get('text')

		# Вызываем метод поиска в базе данных
		with Database() as db:
			search_result = db.search_dream(column, text)
			search_result_metadata = []
			for dream_metadata in search_result:
				metadata = extract_dream_metadata(dream_metadata)
				metadata['description'] = metadata.pop('mood')
				search_result_metadata.append(metadata)

		# Возвращаем результаты в формате JSON
		return jsonify({'success': True, 'results': search_result_metadata})
	except Exception as e:
		return jsonify({'success': False, 'error_message': str(e)})

############
# Страница галереи
############

@app.route('/image/<folder>/<filename>')
def image(folder, filename):
	return send_from_directory(app.config[folder], filename)

@app.route('/upload_image/<sender>/<folder>', methods=['POST'])
def upload_image(sender, folder):
	# Сохраняем файлы на сервер
	access_responses = []
	fail_responses = []

	with Database() as db:
		uploaded_images = request.files.getlist('images')
		# Фильтруем изображения, чтобы оставить только те, которые не пусты
		valid_images = [uploaded_image for uploaded_image in uploaded_images if uploaded_image.filename]
		if valid_images:
			for valid_image in valid_images:
				match sender:
					case 'arts':
						if db.check_art(valid_image.filename):
							db.create_art(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})
							access_responses.append({'filename': valid_image.filename})
						else:
							fail_responses.append({'filename': valid_image.filename, 'error_message': 'Файл із такою назвою вже існує на сервері'})
							continue
					case 'screenshots':
						if db.check_screenshot(valid_image.filename):
							db.create_screenshot(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})
							access_responses.append({'filename': valid_image.filename})
						else:
							fail_responses.append({'filename': valid_image.filename, 'error_message': 'Файл із такою назвою вже існує на сервері'})
							continue
					case 'photos':
						if db.check_photo(valid_image.filename):
							db.create_photo(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})
							access_responses.append({'filename': valid_image.filename})
						else:
							fail_responses.append({'filename': valid_image.filename, 'error_message': 'Файл із такою назвою вже існує на сервері'})
							continue
					case 'codesnaps':
						if db.check_codesnap(valid_image.filename):
							db.create_codesnap(valid_image.filename, {'type': valid_image.filename.split('.')[-1].upper()})
							access_responses.append({'filename': valid_image.filename})
						else:
							fail_responses.append({'filename': valid_image.filename, 'error_message': 'Файл із такою назвою вже існує на сервері'})
							continue

				filename = os.path.join(app.config[folder], valid_image.filename)
				valid_image.save(filename)

				# Открываем изображение
				original_image = Image.open(filename)

				# Создаем миниатюру с максимальным размером 128x128
				image_thumbnail = original_image.copy()
				image_thumbnail.thumbnail((128, 128))

				# Сохраняем миниатюру в директорию thumbnail
				image_thumbnail.save(os.path.join(app.config[f'THUMBNAIL_{folder}'], valid_image.filename))

	# Используем генератор для возврата ответов
	if len(fail_responses) == 0:
		# Если есть хотя бы одна успешная загрузка, вернем общий успех
		return jsonify({'success': True, 'access': access_responses})
	else:
		# Вернем все неуспешные загрузки
		return jsonify({'success': False, 'fail': fail_responses, 'access': access_responses})

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
				case 'CODESNAPS_FOLDER':
					db.remove_codesnap(filename)
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

def get_content(file_name):
	with open(f"{os.path.join(app.config['CONTENT_FOLDER'], file_name)}.md", 'r', encoding='utf-8') as content_file:
		content_data = content_file.read()

	return content_data

def get_posts(post_limit):
	with Database() as db:
		posts = db.get_all_posts(limit=post_limit)
		posts_metadata = [extract_post_metadata(post_metadata) for post_metadata in posts]

	return posts_metadata

def load_post_content(title):
	with Database() as db:
		chosen_post = db.get_post(title)
		chosen_post_metadata = extract_post_metadata(chosen_post)

	# Прочитайте содержимое файла
	with open(f"{os.path.join(app.config['POST_FOLDER'], chosen_post_metadata['title'])}.md", 'r', encoding='utf-8') as post_file:
		chosen_post_metadata['content'] = post_file.read()

	return chosen_post_metadata

def extract_post_metadata(post_obj):
	return {
		'title': post_obj.title,
		'description': post_obj.description,
		'tags': post_obj.tags.split(", "),
		'importance': post_obj.importance,
		'created_at': post_obj.created_at.strftime('%Y-%m-%d %I:%M %p'),
		'published_at': post_obj.published_at.strftime('%Y-%m-%d %I:%M %p'),
		'last_changed_at': post_obj.last_changed_at.strftime('%Y-%m-%d %I:%M %p') if post_obj.last_changed_at is not None else None,

		'files': [{'id': file.id, 'name': file.name, 'type': file.type} for file in post_obj.files]
	}

def get_dreams(dream_limit):
	with Database() as db:
		dreams = db.get_all_dreams(limit=dream_limit)
		dreams_metadata = [extract_dream_metadata(dream_metadata) for dream_metadata in dreams]

	return dreams_metadata

def load_dream_content(title):
	with Database() as db:
		chosen_dream = db.get_dream(title)
		chosen_dream_metadata = extract_dream_metadata(chosen_dream)

	# Прочитайте содержимое файла
	with open(f"{os.path.join(app.config['DREAM_FOLDER'], chosen_dream_metadata['title'])}.md", 'r', encoding='utf-8') as dream_file:
		chosen_dream_metadata['content'] = dream_file.read()

	return chosen_dream_metadata

def extract_dream_metadata(dream_obj):
	return {
		'title': dream_obj.title,
		'mood': dream_obj.mood,
		'tags': dream_obj.tags.split(", "),
		'importance': dream_obj.importance,
		'dreamed_at': dream_obj.dreamed_at.strftime('%Y-%m-%d %I:%M %p'),
		'published_at': dream_obj.published_at.strftime('%Y-%m-%d %I:%M %p')
	}

############
# Запуск блога
############

if __name__ == '__main__':
	app.run(
		host='192.168.0.102',
		port=5000,
		ssl_context=('ssl.crt', 'ssl.key'),
		debug=True
	)
