# Copyright © 2023 Kalynovsky Valentin. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum, ForeignKey, desc
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Posts(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	description = Column(String, nullable=False)
	tags = Column(String, nullable=False)
	importance = Column(Enum('Normal', 'Rare', 'Elite', 'Super Rare', 'Ultra Rare'), nullable=False)
	created_at = Column(DateTime, nullable=False)
	published_at = Column(DateTime)
	last_changed_at = Column(DateTime)

	# Добавим отношение к таблице файлов
	files = relationship("Files", secondary="post_file_association")

class Files(Base):
	__tablename__ = "files"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	type = Column(String, nullable=False)

	# Добавим обратное отношение к таблице постов
	posts = relationship("Posts", secondary="post_file_association", overlaps="files")

class PostFileAssociation(Base):
	__tablename__ = "post_file_association"
	post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
	file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)

class Dreams(Base):
	__tablename__ = "dreams"
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	mood = Column(String, nullable=False)
	tags = Column(String, nullable=False)
	importance = Column(Enum('Normal', 'Rare', 'Elite', 'Super Rare', 'Ultra Rare'), nullable=False)
	dreamed_at = Column(DateTime, nullable=False)
	published_at = Column(DateTime)

class Arts(Base):
	__tablename__ = "arts"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	type = Column(String, nullable=False)

class Screenshots(Base):
	__tablename__ = "screenshots"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	type = Column(String, nullable=False)

class Photos(Base):
	__tablename__ = "photos"
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	type = Column(String, nullable=False)

class Database:
	def __init__(self):
		super(Database, self).__init__()

		self.engine = create_engine("sqlite:///db\\blog_database.db")
		Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	def close(self):
		self.session.close()

	# Методы для работы с таблицей постов

	def get_post(self, title):
		return self.session.query(Posts).filter_by(title=title).first()

	def get_all_posts(self):
		return self.session.query(Posts).order_by(desc(Posts.created_at)).all()

	def check_post(self, title):
		existing_user = self.session.query(Posts.title).filter_by(title=title).scalar()
		return existing_user is None

	def create_post(self, title, post_data):
		new_post = Posts(title=title, **post_data)
		self.session.add(new_post)
		self.session.commit()

	def update_post(self, title, new_data):
		post = self.get_post(title)
		if post:
			# Оновлюємо поля посту
			for key, value in new_data.items():
				setattr(post, key, value)

			# Фіксуємо значення в БД
			self.session.commit()

	def remove_post(self, title):
		post = self.session.query(Posts).filter_by(title=title).first()
		if post:
			self.session.delete(post)
			self.session.commit()

	# Методы для работы с таблицей файлов

	def get_file(self, name):
		return self.session.query(Files).filter_by(name=name).first()

	def get_all_files(self):
		return self.session.query(Files).all()

	def check_file(self, name):
		existing_file = self.session.query(Files.name).filter_by(name=name).scalar()
		return existing_file is None

	def create_file(self, name, post_data):
		new_file = Files(name=name, **post_data)
		self.session.add(new_file)
		self.session.commit()

	def remove_file(self, name):
		file = self.session.query(Files).filter_by(name=name).first()
		if file:
			self.session.delete(file)
			self.session.commit()

	# Методы для работы с таблицей сновидений

	def get_dream(self, title):
		return self.session.query(Dreams).filter_by(title=title).first()

	def get_all_dreams(self):
		return self.session.query(Dreams).order_by(desc(Dreams.dreamed_at)).all()

	def check_dream(self, title):
		existing_user = self.session.query(Dreams.title).filter_by(title=title).scalar()
		return existing_user is None

	def create_dream(self, title, dream_data):
		new_dream = Dreams(title=title, **dream_data)
		self.session.add(new_dream)
		self.session.commit()

	def update_dream(self, title, new_data):
		dream = self.get_dream(title)
		if dream:
			# Оновлюємо поля сновидіння
			for key, value in new_data.items():
				setattr(dream, key, value)

			# Фіксуємо значення в БД
			self.session.commit()

	def remove_dream(self, title):
		dream = self.session.query(Dreams).filter_by(title=title).first()
		if dream:
			self.session.delete(dream)
			self.session.commit()

	# Методы для работы с таблицей артов

	def get_art(self, name):
		return self.session.query(Arts).filter_by(name=name).first()

	def get_all_arts(self):
		return self.session.query(Arts).all()

	def check_art(self, name):
		existing_user = self.session.query(Arts.name).filter_by(name=name).scalar()
		return existing_user is None

	def create_art(self, name, art_data):
		new_art = Arts(name=name, **art_data)
		self.session.add(new_art)
		self.session.commit()

	def remove_art(self, name):
		art = self.session.query(Arts).filter_by(name=name).first()
		if art:
			self.session.delete(art)
			self.session.commit()

	# Методы для работы с таблицей скринов

	def get_screenshot(self, name):
		return self.session.query(Screenshots).filter_by(name=name).first()

	def get_all_screenshots(self):
		return self.session.query(Screenshots).all()

	def check_screenshot(self, name):
		existing_screenshot = self.session.query(Screenshots.name).filter_by(name=name).scalar()
		return existing_screenshot is None

	def create_screenshot(self, name, art_data):
		new_screenshot = Screenshots(name=name, **art_data)
		self.session.add(new_screenshot)
		self.session.commit()

	def remove_screenshot(self, name):
		screenshot = self.session.query(Screenshots).filter_by(name=name).first()
		if screenshot:
			self.session.delete(screenshot)
			self.session.commit()

	# Методы для работы с таблицей фотографий

	def get_photo(self, name):
		return self.session.query(Photos).filter_by(name=name).first()

	def get_all_photos(self):
		return self.session.query(Photos).all()

	def check_photo(self, name):
		existing_photo = self.session.query(Photos.name).filter_by(name=name).scalar()
		return existing_photo is None

	def create_photo(self, name, art_data):
		new_photo = Photos(name=name, **art_data)
		self.session.add(new_photo)
		self.session.commit()

	def remove_photo(self, name):
		photo = self.session.query(Photos).filter_by(name=name).first()
		if photo:
			self.session.delete(photo)
			self.session.commit()

	# Методы для работы с таблицей ассоциаций

	def associate_files(self, post_title, selected_file_ids):
		# Получаем созданный пост
		post = self.get_post(post_title)

		# Открепляем все файлы от поста
		post.files = []

		# Привязываем выбранные файлы к посту
		for file_id in selected_file_ids:
			file = self.session.query(Files).filter_by(id=file_id).first()
			if file:
				post.files.append(file)

		self.session.commit()
