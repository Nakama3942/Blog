from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
import markdown2
import yaml
import os
from datetime import datetime

app = Flask(__name__, template_folder='template', static_folder='resources')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'files')

app.secret_key = 'your_secret_key'  # Секретный ключ для подписи сессий
ADMIN_KEY = 'admin_key'  # Ваш ключ для доступа к админским функциям

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

@app.route('/new_post')
def add_post():
	if not is_admin():
		return 'Access Denied'
	return render_template('new_post.html', is_admin=is_admin())

@app.route('/save_post', methods=['POST'])
def save_post_route():
	# warning работает не корректно
	title = request.form['title']
	description = request.form['description']
	content = request.form['content']

	# Сохраняем файлы на сервер
	saved_files = []
	for uploaded_file in request.files.getlist('file'):
		filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
		uploaded_file.save(filename)
		file_metadata = {'name': uploaded_file.filename, 'type': get_file_type(uploaded_file.filename)}
		saved_files.append(file_metadata)

		# Формируем метаданные поста
		post_metadata = f"name: {title}.md\ntitle: {title}\ndatetime: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\ndescription: {description}\nfiles: {files}\n\n#{title}\n\n{content}"

		# Сохраняем метаданные в файл
		post_filename = f"{title}.md"
		with open(os.path.join(app.config['UPLOAD_FOLDER'], post_filename), 'w', encoding='utf-8') as post_file:
			post_file.write(post_metadata)

	return redirect(url_for('diary'))

@app.route('/')
def home():
	post_files = get_posts('posts', 5)
	post_contents = [load_post_metadata(file) for file in post_files]
	return render_template('index.html', post_contents=post_contents, is_admin=is_admin())

@app.route('/diary')
def diary():
	post_files = get_posts('posts', 0)
	post_contents = [load_post_metadata(file) for file in post_files]
	return render_template('diary.html', post_contents=post_contents, is_admin=is_admin())

def get_posts(posts_directory, num_posts):
	post_files = [f for f in os.listdir(posts_directory) if os.path.isfile(os.path.join(posts_directory, f))]
	post_files.sort(key=lambda x: os.path.getmtime(os.path.join(posts_directory, x)), reverse=True)
	if num_posts:
		return post_files[:num_posts]
	else:
		return post_files

def load_post_metadata(post_content):
	post_content = 'posts/' + str(post_content)
	# print(post_content)
	if os.path.exists(post_content):
		with open(post_content, 'r', encoding='utf-8') as file:
			metadata_block = [next(file) for _ in range(4)]
		metadata_list = []
			# print(str(metadata_block))
		if metadata_block:
			for metadata in metadata_block:
				metadata_list.append(yaml.safe_load(metadata))
			# Convert the 'datetime' string to a datetime object
			if 'datetime' in metadata_list[2]:
				metadata_list[2]['datetime'] = datetime.strptime(metadata_list[2]['datetime'], '%Y-%m-%d %I:%M %p')
			print(str(metadata_list))
			return metadata_list
		else:
			return {"title": "Invalid post format"}
	else:
		return "Post not found"

@app.route('/posts/<post_id>')
def post(post_id):
	# Ваш код для загрузки и отображения полного содержания поста
	post_content = load_post_content(post_id)
	return render_template('post.html', post_content=post_content, is_admin=is_admin())

def load_post_content(file_name):
	file_name = 'posts/' + str(file_name)
	# print(file_name)
	if os.path.exists(file_name):
		with open(file_name, 'r', encoding='utf-8') as file:
			metadata_block = [next(file) for _ in range(5)]
			content = file.read()
			content_list = []
			# print(str(metadata_block))
			# print(str(content))
			if metadata_block and content:
				for metadata in metadata_block:
					content_list.append(yaml.safe_load(metadata))
				# Convert the 'datetime' string to a datetime object
				if 'datetime' in content_list[2]:
					content_list[2]['datetime'] = datetime.strptime(content_list[2]['datetime'], '%Y-%m-%d %I:%M %p')
				content_list.append({'post': yaml.safe_load(markdown2.markdown(content))})
				# print(str(content_list))
				return content_list
			else:
				return {"title": "Invalid post format"}
	else:
		return "Post not found"

@app.route('/files/<path:filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
	app.run(debug=True)
