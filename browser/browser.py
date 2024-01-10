import os
import music_tag

ROOT = os.getcwd()
cwd = os.getcwd()

def get_directories():
	global cwd
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

def navigate_cwd_out():
	global cwd
	idx = cwd.rfind('\\')
	if idx != -1 and len(cwd[:idx]) >= len(ROOT):
		cwd = cwd[:idx]
	else:
		print("Could not navigate_cwd_out")
		

def get_song_tuple(item, contents):
	# pass through the filename and directory contents to get the full tuple
	for file in contents:
		if isinstance(file, tuple) and file[3] == item:
			return file

def select(user):
	# user is selected filename
	# contents is cwd contents
	global cwd

	contents = get_directories()

	try:
		item = user
		if item == 'NULL':
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
		print (track_number, album, artist, filename)
		if ".mp3" in filename:
			print("Playing " + artist + " - " + filename[:-4])
			return (track_number, album, artist, filename)
	except Exception as e:
		print("Invalid input.", e)
	finally:
		print()
		print(cwd)


def query():
	while True:
		contents = get_directories(cwd)
		dict = print_contents(contents)
		user = input("> ")


		cwd = select(user, cwd, dict)