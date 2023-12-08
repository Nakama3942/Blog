from flask import Flask, render_template
import markdown2
import yaml
import os
from datetime import datetime

app = Flask(__name__, template_folder='template', static_folder='resources')

@app.route('/')
def home():
	post_files = get_posts('posts', 5)
	post_contents = [load_post_metadata(file) for file in post_files]
	return render_template('index.html', post_contents=post_contents)

@app.route('/diary')
def diary():
	post_files = get_posts('posts', 0)
	post_contents = [load_post_metadata(file) for file in post_files]
	return render_template('diary.html', post_contents=post_contents)

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
	return render_template('post.html', post_content=post_content)

def load_post_content(file_name):
	file_name = 'posts/' + str(file_name)
	# print(file_name)
	if os.path.exists(file_name):
		with open(file_name, 'r', encoding='utf-8') as file:
			metadata_block = [next(file) for _ in range(4)]
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

if __name__ == '__main__':
	app.run(debug=True)