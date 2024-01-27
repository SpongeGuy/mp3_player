import tkinter as tk
from time import strftime
import packs.browser as browser
from enum import Enum

LOOP_TIME = 100

WINDOW_HEIGHT = 280
WINDOW_LENGTH = 240

COLOR_GREEN = '#00ff00'
COLOR_GREY = '#1f261e'
COLOR_BLACK = '#000000'
COLOR_WHITE = '#ffffff'
COLOR_BLUE = '#1066cc'
COLOR_PURPLE = '#502ec1'
COLOR_LIGHTGREY = '#cecece'

def color(rgb):
	# translates rgb tuple of int to a hexcode
	r, g, b = rgb
	return f'#{r:02x}{g:02x}{b:02x}'

# ============================window============================


root = tk.Tk()
root.title("MP3 Player")
root.geometry(str(WINDOW_LENGTH) + "x" + str(WINDOW_HEIGHT))
root.configure(bg=COLOR_BLACK)

root.resizable(0, 0)


import sys
if sys.platform == 'win32':
	import os
	from ctypes import windll
	basedir = os.path.dirname(__file__)
	myappid = "sponge.mp3_music.1_0"
	windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	root.iconbitmap(os.path.join(basedir, "spongex64mp3.ico"))

# ============================screens============================
def create_new_frame(master, background=COLOR_BLACK, *args, **kwargs):
	frame = tk.Frame(
		master,
		bg=background,
		*args,
		**kwargs
		)
	return frame

container = create_new_frame(root)
container.grid_columnconfigure(0, weight=1)
container.grid_rowconfigure(0, weight=1)
container.pack(fill=tk.BOTH, expand=True)

player_frame = create_new_frame(container)
for i in range(2):
	player_frame.grid_columnconfigure(i, weight=1)
for i in range(5):
	player_frame.grid_rowconfigure(i, weight=1)
player_frame.grid(column=0, row=0, sticky='nsew')

playlist_frame = create_new_frame(container)
playlist_frame.grid(column=0, row=0, sticky='nsew')

watch_frame = create_new_frame(container)
watch_frame.grid(column=0, row=0, sticky='nsew')

screens = {
	player_frame: False, 
	playlist_frame: False,
	watch_frame: False
}

def update_screen():
	current_screen = None
	for frame in screens:
		if screens[frame] is True:
			current_screen = frame
	if current_screen is None:
		screens[player_frame] = True
		player_frame.tkraise()
		return
	current_screen.tkraise()

def change_screen(screen):
	for frame in screens:
		screens[frame] = False

	if screen in screens:
		screens[screen] = True
	else:
		print(f"{screen} is not a valid screen.")
	update_screen()

def get_current_screen():
	for frame in screens:
		if screens[frame] is True:
			return frame


#change_screen(player_frame)


# ============================fonts============================
from tkinter import font
clock_font = font.Font(family="Digital Display", size=36)
vcr_font = font.Font(family="VCR OSD Mono", size=24)
large_craft_font = font.Font(family="Crafter's Delight", size=16)
craft_font = font.Font(family="Crafter's Delight", size=12)
small_craft_font = font.Font(family="Crafter's Delight", size=10)
tiny_craft_font = font.Font(family="Crafter's Delight", size=8)

# ============================clock============================
label_clock = tk.Label(
	player_frame, 
	font=craft_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK
	)
#label_clock.grid(row=0, column=1, sticky='e')

def clock_loop(label):
	def loop():
		string = strftime('%H:%M:%S %p')
		label.config(text=string)
		label.after(LOOP_TIME, loop)
	loop()

def get_clock_value(value):
	# converts value in seconds to minute clock format
	minutes = 0
	seconds = 0
	minutes, seconds = divmod(value, 60)
	minutes = int(minutes)
	seconds = int(seconds)
	return "{:02d}:{:02d}".format(minutes, seconds)

def get_clock_hour_value(value):
	# converts value in seconds to hour clock format
	hours = 0
	minutes = 0
	seconds = 0
	hours, seconds = divmod(value, 3600)
	minutes, seconds = divmod(value, 60)
	hours = int(hours)
	minutes = int(minutes)
	seconds = int(seconds)
	return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

# ============================player============================
import packs.player as p

playlist = [] # this is a list of filepaths to mp3 files

music = p.MusicPlayer(playlist)

def music_start(index, info):
	music.stop()
	music.playlist = playlist
	music.cwd = browser.cwd
	music.index = index
	music.play()
	stopwatch_reset()

def music_volume_up(event):
	music.volume_up()

def music_volume_down(event):
	music.volume_down()

def music_pause(event):
	if not music.playing:
		music.play()
	elif music.playing and not music.paused:
		music.pause()
	elif music.playing and music.paused:
		music.resume()

def music_ff(event):
	music.fast_forward()

def music_rw(event):
	music.rewind()

def music_stop(event):
	music.stop()
	
def music_next(event):
	music.next_song()

def music_prev(event):
	music.previous_song()
# ============================player interface============================
class CustomProgressbar(tk.Canvas):
	def __init__(self, master=None, width=WINDOW_LENGTH - 1, height=10, bg=COLOR_GREY, fg=COLOR_GREEN):
		super().__init__(master, width=width, height=height, bd=0, highlightthickness=0, bg=bg)
		self.width = width
		self.height = height
		self.bg = bg
		self.fg = fg
		self.rectangle = self.create_rectangle(0, 0, width, height, fill=self.fg)

	def update(self, value):
		# update rectangle size based on value
		if value > 1:
			value = 1
		elif value < 0:
			value = 0
		self.coords(self.rectangle, 0, 0, self.width * value, self.height)


player_label_status = tk.Label(
	player_frame, 
	font=small_craft_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK,
	text="PLAYING"
	)
player_label_status.grid(row=0, column=0, sticky='w')

player_label_now_playing = tk.Label(
	player_frame,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='',
	width=WINDOW_LENGTH,
	anchor='w',
	justify='left',
	height=3,
	)
player_label_now_playing.grid(row=3, column=0, sticky='w', columnspan=3)

player_label_volume = tk.Label(
	player_frame,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='VOLUME',
	anchor='e'
	)
player_label_volume.grid(row=0, column=1, sticky='e')

player_label_volume_number = tk.Label(
	player_frame,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='',
	anchor='e',
	)
player_label_volume_number.grid(row=1, column=1, sticky='en')

from tkinter import ttk

player_progress_bar_frame = ttk.Frame(player_frame, width=WINDOW_LENGTH)
player_progress_bar_frame.grid(row=4, column=0, columnspan=3, sticky='w')

s = ttk.Style()
s.theme_use('clam')
s.configure(
	"red.Horizontal.TProgressbar", 
	foreground=COLOR_GREEN,
	background=COLOR_GREEN,
	troughcolor=COLOR_BLACK,
	)

player_progress_bar = CustomProgressbar(
	player_progress_bar_frame,
	height=5,
	)
player_progress_bar.grid(sticky='nsew',)
player_progress_bar.update(0)

player_label_playlist = tk.Label(
	player_frame,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='Directory'
	)
player_label_playlist.grid(row=5, column=0, sticky='w')

player_label_length = tk.Label(
	player_frame,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text=''
	)
player_label_length.grid(row=5, column=1, sticky='e')

# ============================stopwatch============================
from time import perf_counter
from datetime import datetime

player_label_stopwatch = tk.Label(
	player_frame, 
	font=clock_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK,
	text="00:00"
	)
player_label_stopwatch.grid(row=1, column=0, columnspan=3, sticky='w')

start_time = None
running = False



def stopwatch_start():
	global start_time
	global running
	start_time = perf_counter()
	running = True
	stopwatch_loop()

def stopwatch_pause():
	global running
	running = False

def stopwatch_resume():
	global running
	running = True

def stopwatch_reset():
	global start_time
	global running
	start_time = None
	running = False
	stopwatch_start()

# ============================watch interface============================
watch_frame.grid_columnconfigure(0, weight=1)
watch_frame.grid_rowconfigure(0, weight=1)

watch_status_frame = create_new_frame(
	watch_frame,
	background=COLOR_BLACK
	)
watch_status_frame.grid(row=0, column=0, sticky='nsew', pady=(60, 0), padx=(25, 25))

watch_status_frame.grid_columnconfigure(0, weight=1)

watch_label_stopwatch = tk.Label(
	watch_status_frame, 
	font=clock_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK,
	width=WINDOW_LENGTH,
	text="00:00"
	)
watch_label_stopwatch.grid(row=0, column=0, sticky='ew')

watch_progress_bar_frame = tk.Frame(
	watch_status_frame, 
	width=WINDOW_LENGTH - 50,
	background=COLOR_BLACK,
	)
watch_progress_bar_frame.grid(row=1, column=0, sticky='w')
watch_progress_bar = CustomProgressbar(
	watch_progress_bar_frame,
	height=5,
	)
watch_progress_bar.grid(sticky='nsew', pady=(5, 15))
watch_progress_bar.update(0)

watch_label_band = tk.Message(
	watch_status_frame,
	font=craft_font,
	fg=COLOR_LIGHTGREY,
	bg=COLOR_BLACK,
	width=WINDOW_LENGTH,
	anchor='w',
	text=''
	)
watch_label_band.grid(row=2, column=0, sticky='w')

watch_label_album = tk.Message(
	watch_status_frame,
	font=craft_font,
	fg=COLOR_LIGHTGREY,
	bg=COLOR_BLACK,
	width=WINDOW_LENGTH - 50,
	anchor='w',
	text=''
	)
watch_label_album.grid(row=3, column=0, sticky='w')

watch_label_song = tk.Message(
	watch_status_frame,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	width=WINDOW_LENGTH - 50,
	text=''
	)
watch_label_song.grid(row=4, column=0, sticky='w')


# ============================playlist interface============================

selected_index = 0 # manages current selection on listboxes, should always be an integer

playlist_frame.grid_rowconfigure(0, weight=1)
playlist_frame.grid_rowconfigure(1, weight=1)
playlist_frame.grid_rowconfigure(2, weight=10)

playlist_frame.grid_columnconfigure(0, weight=1)
playlist_frame.grid_columnconfigure(1, weight=1)
playlist_frame.grid_columnconfigure(2, weight=1)
playlist_frame.grid_columnconfigure(3, weight=1)
playlist_frame.grid_columnconfigure(4, weight=1)

playlist_playing_status_label = tk.Label(
	playlist_frame,
	bg=COLOR_BLACK,
	fg=COLOR_WHITE,
	font=craft_font,
	text='▶',
	anchor='s'
	)
playlist_playing_status_label.grid(column=1, row=0, columnspan=2, sticky='nsew')

playlist_progress_bar_frame = ttk.Frame(playlist_frame, width=WINDOW_LENGTH)
playlist_progress_bar_frame.grid(column=0, row=1, columnspan=4, sticky='w')
playlist_progress_bar = CustomProgressbar(
	playlist_progress_bar_frame,
	height=5,
	)
playlist_progress_bar.grid(sticky='nsew',)
playlist_progress_bar.update(0)


playlist_listbox_frame = create_new_frame(playlist_frame)
playlist_listbox_frame.grid(column=0, row=2, columnspan=6, sticky='nsew')

playlist_listbox_frame.grid_rowconfigure(0, weight=1)
playlist_listbox_frame.grid_columnconfigure(0, weight=1)
playlist_listbox_frame.grid_columnconfigure(1, weight=3)
playlist_listbox_frame.grid_columnconfigure(2, weight=1)


playlist_listbox_tracknumbers = tk.Listbox(
	playlist_listbox_frame,
	bg=COLOR_BLACK,
	fg=COLOR_WHITE,
	selectbackground=COLOR_PURPLE,
	width=2,
	font=tiny_craft_font,
	highlightthickness=0,
	borderwidth=0,
	)
playlist_listbox_tracknumbers.grid(column=0, row=0, sticky='nsw')

playlist_listbox_directory = tk.Listbox(
	playlist_listbox_frame,
	bg=COLOR_BLACK,
	fg=COLOR_WHITE,
	selectbackground=COLOR_PURPLE,
	font=tiny_craft_font,
	highlightthickness=0,
	borderwidth=0,
	)
playlist_listbox_directory.grid(column=1, row=0, sticky='nswe')

playlist_listbox_info = tk.Listbox(
	playlist_listbox_frame,
	bg=COLOR_BLACK,
	fg=COLOR_WHITE,
	selectbackground=COLOR_PURPLE,
	font=tiny_craft_font,
	highlightthickness=0,
	borderwidth=0,
	width=2,
	)
playlist_listbox_info.grid(column=2, row=0, sticky='nse')

# ============================graphics loop============================

def stopwatch_loop():
	label = None
	
	def loop():
		global label
		if player_frame == get_current_screen():
			label = player_label_stopwatch
			label['text'] = get_clock_value(music.elapsed_time)
		elif watch_frame == get_current_screen():
			label = watch_label_stopwatch
			label['text'] = get_clock_hour_value(music.elapsed_time)
		
		if music.paused or not music.playing:
			label.config(fg=COLOR_WHITE)
		else:
			label.config(fg=COLOR_GREEN)
		label.after(LOOP_TIME, loop)
	loop()

def graphics_loop():
	def loop():
		song_duration = music.length
		elapsed_time = music.elapsed_time
		progress_value = (elapsed_time / song_duration)
		if player_frame is get_current_screen(): # player_frame
			# player_label_status
			if music.paused:
				player_label_status.config(text="PAUSED")
			elif not music.playing:
				player_label_status.config(text="STOPPED")
			else:
				player_label_status.config(text="PLAYING")

			# player_label_now_playing
			if not music.playing:
				player_label_now_playing['text'] = "Not playing"
			elif music.metadata is not None:
				if music.metadata[2] is not '':
					player_label_now_playing['text'] = str(music.metadata[2]) + "\n" + str(music.metadata[1]) + "\n" + str(music.metadata[3][:-4])
				else:
					player_label_now_playing['text'] = str(music.metadata[3][:-4])
			# progress_bar
			
			player_progress_bar.update(progress_value)

			# player_label_length
			song_length = 0
			if music.playing:
				song_length = music.length
			player_label_length['text'] = get_clock_hour_value(song_length)

			# player_label_volume_number
			player_label_volume_number['text'] = str(int(music.volume * 100))

		elif playlist_frame is get_current_screen(): # playlist_frame
			playlist_progress_bar.update(progress_value)

			# playlist_playing_status_label
			if music.paused:
				playlist_playing_status_label['text'] = '▮▮'
			elif not music.playing:
				playlist_playing_status_label['text'] = '■'
			else:
				playlist_playing_status_label['text'] = '▶'

		elif watch_frame is get_current_screen(): # watch_frame
			watch_progress_bar.update(progress_value)
			if not music.playing:
				watch_label_band['text'] = ""
				watch_label_album['text'] = "Not playing"
				watch_label_song['text'] = ""
			elif music.metadata is not None:
				if music.metadata[2] is not '':
					watch_label_band['text'] = str(music.metadata[2])
					watch_label_album['text'] = str(music.metadata[1])
					watch_label_song['text'] = str(music.metadata[0]) + " - " + str(music.metadata[3][:-4])

		player_frame.after(LOOP_TIME, loop)
	loop()

# ============================player_listbox_directory============================
metadata = [] # this is an analogue to the player_listbox_directory, storing tuples of metadata instead of filenames.

# TODO: ADD ALL THIS CODE TO BROWSER.PY AND MAKE IT INTO A CLASS BC DAMN

total_rows = len(player_frame.grid_slaves())

player_listbox_directory_canvas = tk.Canvas(
	player_frame,
	)
player_listbox_directory_canvas.grid(row=total_rows, column=0, columnspan=3, sticky='s')

player_listbox_directory = tk.Listbox(
	player_listbox_directory_canvas, 
	bg=COLOR_BLACK, 
	fg=COLOR_WHITE,
	selectbackground=COLOR_PURPLE,
	font=craft_font, 
	height=8,
	width=WINDOW_LENGTH,
	highlightthickness=0,
	borderwidth=0,
	)
player_listbox_directory = browser.create_directory_listbox(
	player_listbox_directory_canvas,
	font=craft_font,
	height=8,
	width=WINDOW_LENGTH
	)
player_listbox_directory.pack(side='bottom', fill='x')

def get_listbox():
	listbox = None
	if player_frame == get_current_screen():
		listbox = player_listbox_directory
	elif playlist_frame == get_current_screen():
		listbox = playlist_listbox_directory
	return listbox


def populate_directory_listbox():
	global playlist
	global metadata
	global selected_index
	global contents
	playlist = []
	contents = []
	def populate():
		global contents
		global metadata
		# populate graphical list
		contents = browser.get_items_in_directory(browser.cwd)
		metadata = contents
		listbox = get_listbox()
		if playlist_frame is get_current_screen(): # playlist screen
			playlist_listbox_tracknumbers.delete(0, tk.END)
			playlist_listbox_directory.delete(0, tk.END)
			playlist_listbox_info.delete(0, tk.END)
			for i, item in enumerate(contents):
				tracknumber = ''
				if isinstance(item, tuple):
					tracknumber = item[0]
				displayname = browser.strip_item(item)
				playlist_listbox_tracknumbers.insert(i, tracknumber)
				playlist_listbox_directory.insert(i, displayname)

				filename = browser.get_item_filename(item)
				directory = browser.cwd + "\\" + filename
				amount_of_items_inside = browser.get_amount_of_items_in_directory(directory)
				playlist_listbox_info.insert(i, amount_of_items_inside)
		elif player_frame is get_current_screen(): # player screen
			listbox.delete(0, tk.END)
			for i, item in enumerate(contents):
				item = browser.strip_item(item)
				listbox.insert(i, item)

		# populate playlist list list
		for item in contents:
			if isinstance(item, tuple):
				playlist.append(browser.get_song_filepath(item))
	populate()
	if selected_index >= len(contents):
		selected_index = 0

	update_selection()

	

def handle_enter(event):
	# the OK button
	global metadata
	global selected_index
	listbox = get_listbox()
	try:
		if listbox.curselection() is not ():
			selected_index = listbox.curselection()[0]
		selected_value = metadata[selected_index]
		info = browser.select(selected_value)
		populate_directory_listbox()


		if (info is not None and not str(selected_value) == str(music.metadata)) or (info is not None and not music.playing):
			# if selection is an mp3 file and selection isn't the same as the playing audio, then start player
			music_start(selected_index, info)
	except Exception as e:
		print("Couldn't continue:", e)


def handle_back(event):
	# the CANCEL button
	listbox = get_listbox()
	try:
		if listbox.curselection() is not ():
			selected_index = listbox.curselection()[0]
		browser.navigate_cwd_out()
		populate_directory_listbox()
	except Exception as e:
		print("Couldn't continue:", e)

def on_select(event):
	global selected_index
	listbox = get_listbox()
	# do stuff when selection changes
	contents = browser.get_items_in_directory(browser.cwd)
	selected_index = listbox.curselection()[0]
	selected_value = listbox.get(selected_index)

def select_move_up(event):
	global selected_index
	listbox = get_listbox()
	try:
		selected_index = listbox.curselection()[0]
		if selected_index != 0:
			listbox.selection_clear(first=selected_index, last=selected_index)
			selected_index -= 1
			update_selection()
	except Exception as e:
		print("Couldn't move selection up:", e)

def select_move_down(event):
	global selected_index
	listbox = get_listbox()
	try:
		selected_index = listbox.curselection()[0]
		if selected_index != len(listbox.get(0, "end")) - 1:
			listbox.selection_clear(first=selected_index, last=selected_index)
			selected_index += 1
			update_selection()
	except Exception as e:
		print("Couldn't move selection down:", e)
	



def update_selection():
	global selected_index
	listbox = get_listbox()
	if listbox == None:
		return
	if playlist_frame == get_current_screen():
		playlist_listbox_tracknumbers.see(selected_index)
		playlist_listbox_info.see(selected_index)
	listbox.selection_set(selected_index)
	listbox.activate(selected_index)
	listbox.focus_set()
	listbox.see(selected_index)

# ============================screen manager/swapper============================

def swap_screen(event):
	frames = list(screens.keys())
	for i in range(len(frames)):
		if screens[frames[i]] == True:
			screens[frames[i]] = False
			if i + 1 < len(frames):
				#print("hi")
				screens[frames[i+1]] = True
				break
			else:
				screens[frames[0]] = True
				break
	update_screen()
	populate_directory_listbox()

# ============================keybindings============================
keys = {
	'a': False, 
	's': False, 
	'd': False,
	'f': False,
	'f': False,
	'q': False,
	'w': False,
	'e': False,
	'r': False,
	'Next': False,
	'Prior': False,
}

key_actions = {
# these must be in alphabetical order (i guess in order in utf-8 coding)
	('d', 's'): music_next,
	('a', 's'): music_prev,
	('a', 'd', 's',): music_stop,
	('s',): music_pause,
	('a',): music_rw,
	('d',): music_ff,
	('e',): handle_enter,
	('w',): handle_back,
	('r',): select_move_up,
	('f',): select_move_down,
	('q',): swap_screen,
	('Prior',): music_volume_up,
	('Next',): music_volume_down,
}

def keypress(event):
	keys[event.keysym] = True
	action = tuple(sorted(k for k, v in keys.items() if v))
	if action in map(tuple, sorted(map(sorted, key_actions.keys()))):
		key_actions[action](event)

def keyrelease(event):
	keys[event.keysym] = False

root.bind('<<ListboxSelect>>', on_select)
root.bind('<KeyPress>', keypress)
root.bind('<KeyRelease>', keyrelease)

# ============================main calls============================

change_screen(player_frame)
populate_directory_listbox()
graphics_loop()
stopwatch_loop()
root.mainloop()