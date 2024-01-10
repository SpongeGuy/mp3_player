import os
import music_tag

ROOT = os.getcwd()

def get_directories(directory):
	contents = []
	# if .mp3, sort by tracknumber then album
	for filename in os.listdir(directory):
		if filename.endswith('.mp3'):
			song = music_tag.load_file(os.path.join(directory, filename))
			contents.append((song['tracknumber'].first, song['album'], song['artist'], filename))
	contents.sort()
	for filename in os.listdir(directory):
		if not filename.endswith('.mp3'):
			contents.append(filename)
	return contents

def print_contents(contents):
	dict = {}
	id = 1
	for file in contents:
		dict[id] = file
		id += 1

	for key in dict:
		if isinstance(dict[key], tuple):
			print(key, dict[key][3])
		else:
			print(key, dict[key])

	return dict

def navigate_cwd_out(dir):
	idx = dir.rfind('\\')
	if idx != -1 and len(dir[:idx]) >= len(ROOT):
		return dir[:idx]
	else:
		print("Could not navigate_cwd_out")
		return dir
		

cwd = os.getcwd()

def select(user, dir, dict):
	if user == '..':
			dir = navigate_cwd_out(dir)
			print()
			print(dir)
			return dir
	try:
		item = dict.get(int(user), 'NULL')
		if item == 'NULL':
			raise Exception('invalid selection from dictionary')

		if not isinstance(item, tuple):
			if "." in item:
				print("Cannot open file", item)
			else:
				dir = os.path.join(dir, item)

		track_number = item[0]
		album = str(item[1])
		artist = str(item[2])
		filename = item[3]
		if ".mp3" in filename:
			print("Playing " + artist + " - " + filename[:-4])
	except Exception as e:
		print("Invalid input.", e)
	finally:
		print()
		print(dir)
		return dir


def query():
	while True:
		contents = get_directories(cwd)
		dict = print_contents(contents)
		user = input("> ")


		cwd = select(user, cwd, dict)