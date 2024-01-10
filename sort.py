import os
import music_tag

cwd = "D:\\Music\\C418\\Beta"

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
	print(contents)
	return contents

def print_contents(contents):
	id = 1
	for item in contents:
		if isinstance(item, tuple):
			print(str(id) + ". " + item[2])
			id += 1
		else:	
			print(str(id) + ". " + str(item))
			id += 1

#get_directories(cwd)
print_contents(get_directories(cwd))



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
			if "." in filename:
				print("Cannot open file", item)
			else:
				dir = os.path.join(dir, filename)

		
		track_number = item[0]
		album = item[1]
		artist = item[2]
		filename = item[3]
		if ".mp3" in filename:
			print("Playing " + artist + " - " + filename[:-4])


'''
def select(a, dir, dict):
	if a == '..':
			dir = navigate_cwd_out(dir)
			print()
			print(dir)
			return dir
	
	try:
		filename = dict.get(int(a), 'NULL')
		if filename == 'NULL':
			raise Exception('invalid selection from dictionary')
		if ".mp3" in filename:
			print("Playing", filename)
		elif "." in filename:
			print("Cannot open file", filename)
		else:
			dir = os.path.join(dir, filename)
	except Exception as e:
		print("Invalid input.")
	finally:
		print()
		print(dir)
		return dir