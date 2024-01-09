# Start of Blog development - v0.0.1

The functionality for displaying the list of posts and the posts themselves has been implemented, and the main page template has been implemented. Three pages are currently available: Home, Diary, Post.

# Page structure update - v0.0.2

The page structure has been optimized, the display of attached post files has been implemented, and the footer has been updated; The repository structure has been changed.

# Post creation update - v0.0.3

Added admin login and post adding page.

# Database update - v0.1.0

Added a database of posts and fixed the saving of posts; rewrote all post-processing code.

# Yourself update - v0.2.0

Improved design.
Added:
1. Description about yourself;
2. Simplified frames;
3. Templates for all scheduled pages.
Filled out the autobiography, projects and documentation.

# Private update - v0.2.1

Made it possible to make posts private, expanded the logic for deleting posts, removed permanently keeping the database open.

# Files update - v0.3.0

Changed how files work: now files are uploaded and deleted from a separate page and can be pinned to posts. A new principle of downloading files has been implemented and the database module has been updated. A table of connections between posts and files has been implemented.

# Privacy logic update - v0.4.0

Improved server code.

Changed privacy logic: now posts after creation are always private at first and become public only after clicking the new "publish" button after saving the post. Pressing the same button again returns the status of the post to "private".

# Videoblog update - v0.5.0

Implemented a page displaying the Videoblog playlist and fixed several bugs:
1. Removed centering of post content field when field height exceeds screen height;
2. In the list of posts, corrected the old post_datetime to the new created_at.

# Art update - v0.6.0

Added:
1. Basic page template;
2. An art page with full functionality.
Created a table in the database for the dream page.

# Technical update - v0.6.1

Changed the navbar, prepared add a gallery, and fixed a few bugs:
1. Removed the code I previously forgot to remove on the post update page;
2. Now when saving a post, the number of line breaks in the content does not double;
3. Images from the gallery can now be displayed in posts.

# Gallery update - v0.6.2

Converted the art page into a multitasking page capable of displaying different content.

# Improvements update - v0.7.0

Improvements and bug fixes:
1. Removed the arts.html file I forgot to remove;
2. Moved the playlist id to .env;
3. Moved the initial documentation to the navbar itself and removed the old page;
4. Improved navbar;
5. Implemented a modal window for displaying a list of posts to which a file is pinned, with the option of opening a post;
6. File uploads have been moved to a modal window.

# Navbar update - v0.7.1

Expanded the navbar.

# Diary update - v0.8.0

Added a dream diary:
1. Based on the post diary, I created a dream diary;
2. After creating a dream diary, I tested the post diary - I had to rewrite it almost from scratch: the technology of Flask forms was studied and HTML forms were replaced when creating and updating posts and dreams on Flask forms;
3. Fixed bug with scripts import;
4. Added tags and importance to posts;
5. Rewrote half of the code on the server to add support for updated posts and dreams;
6. Colors for the frames and background of a post/dream are now highlighted depending on the importance of the post (in dreams - quality);
7. Added a copy of the style without color highlights (not updated for further changes);
8. Added functionality that makes it easier to add images to post text.

# Global update - v0.9.0

Improvements made:
1. Updated video blog loading (playlist ID moved to navbar), making it easier to add new playlists to navbar;
2. I rewrote "About myself";
3. Changed the placement of tags in the tag block, moving it inline with the tag block;
4. Added display of tags in the list of posts and dreams;
5. The principle of "Confidentiality" has been revised:
	1. Removed is_private from database;
	2. Posts are now always public, but can be hidden from everyone by adding the first "Private" tag;
	3. If this tag is present, only the blog owner will see it;
	4. Since posting is no longer required, the buttons and features for posting posts and dreams have been removed;
	5. The date of publication is considered the date of saving, and the date of writing, as before, can be any date (what if I had a diary from 10 years ago and I want to transfer my entries from there to the Blog?);
	6. According to this logic, I added the date of publication of dreams;
6. Now you cannot create posts and dreams with the same name; also cannot upload files and images with the same names:
	1. Posts and dreams will simply not be saved and a warning will be displayed saying that saving is not complete - just change the name;
	2. Files and images, if they were uploaded with those names, simply won't load;
	3. Processed the result of saving a post/dream on the client;
7. Removed post_path and dream_path - there is no point in saving them, since the paths to all the necessary directories are stored on the server, and the name is stored in the database - when the path is needed, it can be reassembled from the desired path and name;
8. Fixed a bug on the post update page when the post creation time is reset because the field does not store seconds and milliseconds; made so that when saving updates, dates and times are compared, ignoring seconds and milliseconds; if they are equal, the publication creation date does not change;
9. Fixed errors in styles;
10. In a separate styles file, I removed all the styles, leaving only the style that turns off the colors and animations of the post and dream frames;
11. Rewrote half of the server code to support updates.

# Optimization update - v0.10.0

The following improvements have been made:
1. Files and gallery moved to request system, as with messages and images:
	1. Now files and images cannot be uploaded with the same names either;
	2. Now the blog admin will know which files/images have been uploaded and which have not;
2. The database was refactored;
3. Getting the list of recent publications for the main page has been optimized;
4. Fixed the basic template;
5. I gave up on the idea of publishing the code (otherwise I would have to go the same way as with the dream journal):
	1. I decided to leave only CodeSnaps in the finished gallery;
	2. Changed the navbar;
	3. Added a new table to the database for CodeSnaps.

# Search update - v0.11.0

Implemented search by title, description and tags for posts and dreams.

Now the server starts on the local network.

# Button update - v0.11.1

Replaced form buttons with regular buttons and moved the delete button to the modal window.

# Articles update - v0.12.0

Made improvements to the Blog pages:
1. Surrounded all Articles with Div class="article-container"
2. Fixed all bugs in the navbar
3. Refused to add navbar animation
4. Fixed bugs in forms
5. Corrected the order of elements of the Post/Dream creation forms
6. Now you can clearly see the background color of a Post/Dream even in the process of creating/changing them
7. Corrected the styles and removed errors in them

# Favicon update - v0.12.1

Split the styles file into several files, fixed new bugs in the navbar and added:
1. Favicon;
2. Display of the last five dreams on the main page.

# Settings update - v0.13.0

Implemented a settings panel and a toggle to disable all styles.

# Meme update - v0.13.1

Removed toggle from the form style (bug fixed) and added new settings:
1. Implemented a color switch for frames (on the pages of creating/editing a post/dream you cannot turn off the color of the frames);
2. Added an avatar to the header;
3. Implemented a meme mode switch;
4. Returned broken frames in meme mode;
5. Fixed the order of the toggles.

# Style structure update - v0.13.2

Changed the style structure (prepared addition a dark theme) and finished adding settings (the styles themselves have not yet been rewritten and look disgusting).

# Final update - v0.13.3

1. Fixed styles:
	1. Made changes to the icon structure
	2. Added icons for toggles
	3. Hid the tooltips in the mode with css enabled
2. Changed the principle of enabling the dark theme
3. Combined forms into one file
4. Refused optimizations:
	1. Loading data is not critical now
	2. There is a problem with searching in the library itself - it only supports the Latin alphabet, therefore in the Cyrillic alphabet only case-sensitive search is possible and this cannot be solved in any way...
