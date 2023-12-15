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

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Post(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True)
	title = Column(String)
	description = Column(String)
	files = Column(String)
	post_datetime  = Column(DateTime)
	post_path  = Column(String)

class PostDb:
	def __init__(self):
		super(PostDb, self).__init__()

		self.engine = create_engine(f"sqlite:///db\\posts_database.db")
		Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind=self.engine)
		self.session = self.Session()

	def get_post(self, title):
		return self.session.query(Post).filter_by(title=title).first()

	def get_all_posts(self):
		return self.session.query(Post).all()

	def check_post(self, title):
		existing_user = self.session.query(Post.title).filter_by(title=title).scalar()
		return existing_user is None

	def create_post(self, title, post_data):
		new_post = Post(title=title, **post_data)
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
		post = self.session.query(Post).filter_by(title=title).first()
		if post:
			self.session.delete(post)
			self.session.commit()

	def close(self):
		self.session.close()
