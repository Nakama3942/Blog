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

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Posts(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True)
	title = Column(String)
	description = Column(String)
	post_datetime = Column(DateTime)
	post_path = Column(String)
	is_private = Column(Boolean)

	# Связь с таблицей Files
	file_id = Column(Integer, ForeignKey('files.id'))
	file = relationship("Files", back_populates="posts")

class Files(Base):
	__tablename__ = "files"
	id = Column(Integer, primary_key=True)
	name = Column(String)
	type = Column(String)

	# Связь с таблицей Posts
	posts = relationship("Posts", back_populates="file")
	# Количество ссылок на этот файл
	references_count = Column(Integer, default=0)

class Database:
	def __init__(self):
		super(Database, self).__init__()

		self.posts_engine = create_engine("sqlite:///db\\posts_database.db")
		Base.metadata.create_all(self.posts_engine)
		self.PostsSession = sessionmaker(bind=self.posts_engine)
		self.postsSession = self.PostsSession()

		self.files_engine = create_engine("sqlite:///db\\files_database.db")
		Base.metadata.create_all(self.files_engine)
		self.FilesSession = sessionmaker(bind=self.files_engine)
		self.filesSession = self.FilesSession()

	def close(self):
		self.postsSession.close()
		self.filesSession.close()

	# Методы для работы с таблицей постов

	def get_post(self, title):
		return self.postsSession.query(Posts).filter_by(title=title).first()

	def get_all_posts(self):
		return self.postsSession.query(Posts).all()

	def check_post(self, title):
		existing_user = self.postsSession.query(Posts.title).filter_by(title=title).scalar()
		return existing_user is None

	def create_post(self, title, post_data):
		new_post = Posts(title=title, **post_data)
		self.postsSession.add(new_post)
		self.postsSession.commit()

	def update_post(self, title, new_data):
		post = self.get_post(title)
		if post:
			# Оновлюємо поля посту
			for key, value in new_data.items():
				setattr(post, key, value)

			# Фіксуємо значення в БД
			self.postsSession.commit()

	def remove_post(self, title):
		post = self.postsSession.query(Posts).filter_by(title=title).first()
		if post:
			self.postsSession.delete(post)
			self.postsSession.commit()

	# Методы для работы с таблицей файлов

	def get_file(self, name):
		return self.filesSession.query(Files).filter_by(name=name).first()

	def get_all_files(self):
		return self.filesSession.query(Files).all()

	def check_file(self, name):
		existing_user = self.filesSession.query(Files.name).filter_by(name=name).scalar()
		return existing_user is None

	def create_file(self, name, post_data):
		new_file = Files(name=name, **post_data)
		self.filesSession.add(new_file)
		self.filesSession.commit()

	def remove_file(self, name):
		file = self.filesSession.query(Files).filter_by(name=name).first()
		if file:
			self.filesSession.delete(file)
			self.filesSession.commit()
