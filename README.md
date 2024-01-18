[![GitHub license](https://img.shields.io/github/license/Nakama3942/ALGOR?color=gold&style=flat-square)](https://github.com/Nakama3942/Blog/blob/main/LICENSE)

[![CHANGELOG](https://img.shields.io/badge/here-CHANGELOG-yellow)](https://github.com/Nakama3942/Blog/blob/main/CHANGELOG.md)
[![CONTRIBUTING](https://img.shields.io/badge/here-CONTRIBUTING-indigo)](https://github.com/Nakama3942/Blog/blob/main/CONTRIBUTING.md)
[![CODE_OF_CONDUCT](https://img.shields.io/badge/here-CODE_OF_CONDUCT-darkgreen)](https://github.com/Nakama3942/Blog/blob/main/CODE_OF_CONDUCT.md)
[![PULL_REQUEST_TEMPLATE](https://img.shields.io/badge/here-PULL_REQUEST_TEMPLATE-orange)](https://github.com/Nakama3942/Blog/blob/main/.github/PULL_REQUEST_TEMPLATE.md)

# Blog
## Content
- [Blog](#blog)
	- [Content](#content)
	- [Overview](#overview)
	- [LICENSE](#license)
	- [Thanks](#thanks)
	- [Install](#install)
	- [Troubleshooting](#troubleshooting)
	- [Authors](#authors)

## Overview
I've been wanting to keep my own diary for a long time. But writing on paper is somehow no longer fashionable and outdated. It was possible to use a specialized program, but only I would see my diary. And I wanted it to be public! So that anyone could come in and read, for example, what I did yesterday. This is where a personal blog fits perfectly. But I didn't want to use a ready-made template. I wanted to stand out like developers did in the 90s. I wanted to write something of my own. This is how this blog came about.

## LICENSE
The full text of the license can be found at the following [link](https://github.com/Nakama3942/Blog/blob/main/LICENSE).

> Copyright © 2023-2024 Kalynovsky Valentin. All rights reserved.
> 
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
> 
>     http://www.apache.org/licenses/LICENSE-2.0
> 
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.

## Thanks
Thanks to Krisada for providing the free icon pack. You helped me out a lot!
https://www.deviantart.com/krisada/art/SATORI-File-Type-Icon-546526945

## Install
If you want to use my site as the core of your own, I will tell you how to modify it.

First you need to install the following libraries:

```
pip install flask
pip install flask-wtf
pip install python-dotenv
pip install SQLAlchemy
pip install markdown2
pip install Pillow
```

If you download a ready-made archive, you will receive a ready-made empty _content_ directory, but if you clone a repository, this directory must be created manually. Here is her tree:

```
📦content
 ┣ 📂db
 ┣ 📂docs
 ┣ 📂dreams
 ┣ 📂files
 ┣ 📂gallery
 ┃ ┣ 📂arts
 ┃ ┃ ┗ 📂thumbnails
 ┃ ┣ 📂codesnaps
 ┃ ┃ ┣ 📂thumbnails
 ┃ ┣ 📂photos
 ┃ ┃ ┗ 📂thumbnails
 ┃ ┗ 📂screenshots
 ┃ ┃ ┣ 📂thumbnails
 ┣ 📂posts
 ┣ 📜biography.md
 ┣ 📜index.md
 ┗ 📜projects.md
```

Content only needs to be filled in the _biography.md_, _index.md_ and _projects.md_ files. The remaining directories should be empty. The files there will be created themselves during the blog’s operation. The contents of the _biography.md_ and _index.md_ files will be converted to HTML, which uses the same styles. Therefore, it is enough to remember that the headings are formatted like this:

```
<h1 class="title">Про себе</h1>
<h3 class="subtitle">♟️ Хобі</h3>
```

Otherwise, these files are written exactly the same as standard Markdown files.

The _projects.md_ file is designed completely differently. Five keys are used to form a project list element. Therefore, to create a dictionary for each project, you need to describe five list elements in the file itself. Here is an example of a list of two projects:

```
* Normal
* https://first_link.com/
* Name for first project
* Description for first project
* Date for first project: 01.01.2024 - 02.01.2024
* Normal
* https://second_link.com/
* Name for second project
* Description for second project
* Date for first project: 03.01.2024 - 04.01.2024
```

Instead of Normal, you can also enter _Rare_, _Elite_, _Super Rare_, _Ultra Rare_. This only affects the color of the frame.

Next you need to create an environment file _.env_ next to _index.py_, in which you need to enter the variables:

```
SECRET_KEY=some_secret_key
ADMIN_KEY=some_admin_key

YOUTUBE_API_KEY=some_youtube_api_key
```

After _=_ you need to enter your value. The _YOUTUBE_API_KEY_ variable can be omitted, but then YouTube playlists will not work. Playlist IDs are indicated in the navigation bar in _base.html_. After specifying _SECRET_KEY_ and _ADMIN_KEY_, you can log in to the Administrator. To do this, in the link field you need to enter ```login?key=some_admin_key``` to log in and ```logout``` to log out of the Administrator role.

And finally, to start the server you need a key and a security certificate. Name them _ssl.key_ and _ssl.crt_ respectively. You can generate it yourself:

```
openssl genpkey -algorithm RSA -out local.key

openssl req -new -key local.key -out local.csr

openssl x509 -req -days 365 -in local.csr -signkey local.key -out local.crt
```

If you want to publish a website on the Internet, it is better to buy these certificates from a special service. If you want to give up encryption and switch from https to http, just remove line 693 ```ssl_context=('ssl.crt', 'ssl.key'),```:

```
if __name__ == '__main__':
	app.run(
		host='192.168.0.102',
		port=5000,
		debug=True
	)
```

These steps need to be done in order for the entire site to fully function. If you want to make more changes (which you will want), it is assumed that you understand Fullstack Web development and will be able to make the necessary changes in both the server and the client. I (the Author of this blog) cannot know exactly what changes you may need and provide the necessary functionality for modification. I developed this site primarily for myself.

## Troubleshooting
All algorithms have been tested by me, but if you have problems using the library, the code does not work, have suggestions for optimization or advice to improve the style of the code and the name - I invite you [here](https://github.com/Nakama3942/Blog/blob/main/CONTRIBUTING.md) and [here](https://github.com/Nakama3942/Blog/blob/main/CODE_OF_CONDUCT.md).

## Authors
<table align="center" style="border-width: 10; border-style: ridge">
	<tr>
		<td align="center"><a href="https://github.com/Nakama3942"><img src="https://avatars.githubusercontent.com/u/73797846?s=400&u=a9b7688ac521d739825d7003a5bd599aab74cb76&v=4" width="150px;" alt=""/><br /><sub><b>Kalynovsky Valentin</b></sub></a><sub><br />"Ideological inspirer and Author"</sub></td>
		<!--<td></td>-->
	</tr>
<!--
	<tr>
		<td></td>
		<td></td>
	</tr>
-->
</table>
