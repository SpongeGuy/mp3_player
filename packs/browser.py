import os
import music_tag
import tkinter as tk

ROOT = os.getcwd()
cwd = os.getcwd()

COLOR_GREEN = '#00ff00'
COLOR_GREY = '#1f261e'
COLOR_BLACK = '#000000'
COLOR_WHITE = '#ffffff'
COLOR_BLUE = '#502ec1'


def get_items_in_directory(dir):
	# returns list of filenames or tuples
	# adds filename if file is not mp3
	# adds tuple if file is mp3

	contents = []
	# if .mp3, sort by tracknumber then album
	for filename in os.listdir(dir):
		if filename.endswith('.mp3'):
			song = music_tag.load_file(os.path.join(dir, filename))
			try:
				tracknumber = int(song['tracknumber'].first)
			except Exception:
				tracknumber = 0
			try:
				album = str(song['album'])
			except Exception:
				album = ''
			try:
				artist = str(song['artist'])
			except Exception:
				artist = ''
			contents.append((tracknumber, album, artist, filename))
	contents.sort()
	for filename in os.listdir(dir):
		if not filename.endswith('.mp3'):
			contents.append(filename)
	return contents

def get_amount_of_items_in_directory(dir):
	count = 0
	try:
		for item in os.listdir(dir):
			count += 1
	except Exception as e:
		# this will happen if dir is invalid
		count = ''
	return count

def strip_item(item):
	# if item in contents is mp3 tuple, then just take the filename
	# else item is already the filename. change nothing

	if isinstance(item, tuple):
		item = str(item[3])
		if item.endswith('.mp3'):
			item = item[:-4]
	return item

def get_item_filename(item):
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



def get_song_tuple(filename, contents):
	# pass through the filename and directory contents to get the full tuple
	for item in contents:
		if isinstance(item, tuple) and item[3] == filename:
			return item



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



def select(item):
	# user is selected filename
	global cwd
	contents = get_items_in_directory(cwd)

	try:
		if item == None:
			raise Exception('invalid selection from dictionary')

		if isinstance(item, tuple):
			return item

		if "." in item:
			print("Cannot open file", item)
		else:
			cwd = os.path.join(cwd, item)
		return
	except Exception as e:
		print("Invalid input.", e)


# ============================listbox functions============================

def create_directory_listbox(master, bg=COLOR_BLACK, fg=COLOR_WHITE, selectbackground=COLOR_BLUE, highlightthickness=0, borderwidth=0, *args, **kwargs):
	listbox = tk.Listbox(
		master,
		bg=bg,
		fg=fg,
		selectbackground=selectbackground,
		highlightthickness=highlightthickness,
		borderwidth=borderwidth,
		*args, 
		**kwargs
		)
	return listbox

def populate_listbox(listbox, array):
	try:
		if not isinstance(list, array):
			raise Exception("parameter must be a list")
		listbox.delete(0, tk.END)
		for i, item in enumerate(array):
			listbox.insert(i, item)
	except:
		print("Could not populate listbox:", e)