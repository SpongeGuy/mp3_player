import os
import music_tag

ROOT = os.getcwd()
cwd = os.getcwd()

def get_directories(cwd):
	contents = []
	# if .mp3, sort by tracknumber then album
	for filename in os.listdir(cwd):
		if filename.endswith('.mp3'):
			song = music_tag.load_file(os.path.join(cwd, filename))
			contents.append((song['tracknumber'].first, song['album'], song['artist'], filename))
	contents.sort()
	for filename in os.listdir(cwd):
		if not filename.endswith('.mp3'):
			contents.append(filename)
	return contents

def strip_item(item):
	# if item in contents is mp3 tuple, then just take the filename
	# else item is already the filename. change nothing

	if isinstance(item, tuple):
		item = str(item[3])
	return item

def strip_directory(dir):
	# strip a path of its last directory
	idx = dir.rfind('\\')
	if idx != -1 and len(dir[:idx]) >= len(ROOT):
		dir = dir[:idx]
	else:
		print("Could not navigate_cwd_out")
	return dir

def navigate_cwd_out():
	# go back in the cwd
	global cwd
	cwd = strip_directory(cwd)

def get_song_tuple(item, contents):
	# pass through the filename and directory contents to get the full tuple
	for file in contents:
		if isinstance(file, tuple) and file[3] == item:
			return file

def get_song_filepath(item):
	# pass through an mp3 tuple and get the filepath
	global cwd
	if isinstance(item, tuple):
		return os.path.join(cwd, item[3])
	else:
		print("Could not get filepath of song:", "File is not an mp3.")

def get_song_from_filepath(path):
	# pass through a filepath and get the filename
	try:
		if not path.endswith('.mp3'):
			raise Exception("Path does not lead to an mp3 file.")
		return os.path.basename(path)
	except Exception as e:
		print("Could not get song from filepath:", e)



def select(user):
	# user is selected filename
	global cwd

	contents = get_directories(cwd)

	try:
		item = user
		if item == None:
			raise Exception('invalid selection from dictionary')

		if 'mp3' not in item:
			if "." in item:
				print("Cannot open file", item)
			else:
				cwd = os.path.join(cwd, item)
			return

		# it is now known that item is an mp3 file
		# loop through contents and find matching result
		for file in contents:
			if isinstance(file, tuple) and file[3] == item:
					item = file

		track_number = item[0]
		album = str(item[1])
		artist = str(item[2])
		filename = item[3]
		if ".mp3" in filename:
			return item
	except Exception as e:
		print("Invalid input.", e)


def query():
	while True:
		contents = get_directories(cwd)
		dict = print_contents(contents)
		user = input("> ")


		cwd = select(user, cwd, dict)