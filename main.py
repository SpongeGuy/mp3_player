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

# ============================screens============================
def create_new_frame(master):
	frame = tk.Frame(
		master,
		bg=COLOR_BLACK
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
playlist_frame.grid_columnconfigure(1, weight=1)
playlist_frame.grid_rowconfigure(0, weight=1)
playlist_frame.grid(column=0, row=0, sticky='nsew')

downloader_frame = create_new_frame(container)
downloader_frame.grid(column=0, row=0, sticky='nsew')

screens = {
	player_frame: False, 
	playlist_frame: False,
	downloader_frame: False
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
small_craft_font = font.Font(family="Crafter's Delight", size=9)

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

player = p.MusicPlayer(playlist)

def player_start(index, info):
	player.playlist = playlist
	player.cwd = browser.cwd
	player.index = index
	player.stop()
	player.play()
	stopwatch_reset()

def player_volume_up(event):
	player.volume_up()

def player_volume_down(event):
	player.volume_down()

def player_pause(event):
	if not player.playing:
		player.play()
	elif player.playing and not player.paused:
		player.pause()
	elif player.playing and player.paused:
		player.resume()

def player_ff(event):
	player.fast_forward()

def player_rw(event):
	player.rewind()

def player_stop(event):
	player.stop()

def player_next(event):
	player.next_song()

def player_prev(event):
	player.previous_song()

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


label_status = tk.Label(
	player_frame, 
	font=small_craft_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK,
	text="PLAYING"
	)
label_status.grid(row=0, column=0, sticky='w')

label_now_playing = tk.Label(
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
label_now_playing.grid(row=3, column=0, sticky='w', columnspan=3)

label_volume = tk.Label(
	player_frame,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='VOLUME',
	anchor='e'
	)
label_volume.grid(row=0, column=1, sticky='e')

label_volume_number = tk.Label(
	player_frame,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='',
	anchor='e',
	)
label_volume_number.grid(row=1, column=1, sticky='en')

from tkinter import ttk

bar_frame = ttk.Frame(player_frame, width=WINDOW_LENGTH)
bar_frame.grid(row=4, column=0, columnspan=3, sticky='w')

s = ttk.Style()
s.theme_use('clam')
s.configure(
	"red.Horizontal.TProgressbar", 
	foreground=COLOR_GREEN,
	background=COLOR_GREEN,
	troughcolor=COLOR_BLACK,
	)

progress_bar = CustomProgressbar(
	bar_frame,
	height=5,
	)
progress_bar.grid(sticky='nsew',)
progress_bar.update(0)

label_playlist = tk.Label(
	player_frame,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='Directory'
	)
label_playlist.grid(row=5, column=0, sticky='w')

label_length = tk.Label(
	player_frame,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text=''
	)
label_length.grid(row=5, column=1, sticky='e')

def radio_graphics_loop():
	def loop():
		if player_frame is get_current_screen():
			# label_status
			if player.paused:
				label_status.config(text="PAUSED")
			elif not player.playing:
				label_status.config(text="STOPPED")
			else:
				label_status.config(text="PLAYING")

			# label_now_playing
			if not player.playing:
				label_now_playing['text'] = "Not playing"
			if player.metadata is not None:
				if player.metadata[2] is not '':
					label_now_playing['text'] = str(player.metadata[2]) + "\n" + str(player.metadata[1]) + "\n" + str(player.metadata[3][:-4])
				else:
					label_now_playing['text'] = str(player.metadata[3][:-4])
			# progress_bar
			song_duration = player.length
			elapsed_time = player.elapsed_time
			progress_value = (elapsed_time / song_duration)
			progress_bar.update(progress_value)

			# label_length
			song_length = 0
			if player.playing:
				song_length = player.length
			label_length['text'] = get_clock_hour_value(song_length)

			# label_volume_number
			label_volume_number['text'] = str(int(player.volume * 100))
		

		player_frame.after(LOOP_TIME, loop)
	loop()



# ============================stopwatch============================
from time import perf_counter
from datetime import datetime

label_stopwatch = tk.Label(
	player_frame, 
	font=clock_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK,
	text="00:00"
	)
label_stopwatch.grid(row=1, column=0, columnspan=3, sticky='w')

start_time = None
running = False

def stopwatch_loop():
	def loop():
		label_stopwatch['text'] = get_clock_value(player.elapsed_time)
		if player.paused or not player.playing:
			label_stopwatch.config(fg=COLOR_WHITE)
		else:
			label_stopwatch.config(fg=COLOR_GREEN)
		label_stopwatch.after(LOOP_TIME, loop)
	loop()

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

# ============================playlist interface============================

tracknumbers_listbox = tk.Listbox(
	playlist_frame,
	bg=COLOR_BLACK,
	fg=COLOR_WHITE,
	width=3,
	font=craft_font,
	highlightthickness=0,
	borderwidth=0,
	)
tracknumbers_listbox.grid(column=0, row=0, sticky='nsw')

tracks_listbox = tk.Listbox(
	playlist_frame,
	bg=COLOR_GREY,
	fg=COLOR_WHITE,
	font=craft_font,
	highlightthickness=0,
	borderwidth=0,
	)
tracks_listbox.grid(column=1, row=0, sticky='nswe')

info_listbox = tk.Listbox(
	playlist_frame,
	bg=COLOR_BLACK,
	fg=COLOR_WHITE,
	font=craft_font,
	highlightthickness=0,
	borderwidth=0,
	width=3,
	)
info_listbox.grid(column=2, row=0, sticky='nse')


# ============================listbox_main============================
metadata = [] # this is an analogue to the listbox_main, storing tuples of metadata instead of filenames.

total_rows = len(player_frame.grid_slaves())

listbox_main_canvas = tk.Canvas(
	player_frame,
	)
listbox_main_canvas.grid(row=total_rows, column=0, columnspan=3, sticky='s')

listbox_main = tk.Listbox(
	listbox_main_canvas, 
	bg=COLOR_BLACK, 
	fg=COLOR_WHITE,
	selectbackground=COLOR_BLUE,
	font=craft_font, 
	height=8,
	width=WINDOW_LENGTH,
	highlightthickness=0,
	borderwidth=0,
	)
listbox_main.pack(side='bottom', fill='x')

def get_listbox():
	listbox = None
	if player_frame == get_current_screen():
		listbox = listbox_main
	elif playlist_frame == get_current_screen():
		pass
	return listbox


def populate_listbox(listbox, selection):
	global playlist
	global metadata
	playlist = []
	def populate():
		global metadata
		# populate graphical list
		contents = browser.get_items_in_directory(browser.cwd)
		metadata = contents
		listbox.delete(0, tk.END)
		i = 0
		for item in contents:
			item = browser.strip_item(item)
			listbox.insert(i, item)
			i += 1

		# populate playlist list list
		for item in contents:
			if isinstance(item, tuple):
				playlist.append(browser.get_song_filepath(item))
	populate()
	if selection >= listbox.size():
		selection = 0

	change_selection(listbox, selection)

def handle_enter(event):
	# the OK button
	global metadata
	listbox = get_listbox()
	try:
		selected_index = listbox.curselection()[0]
		selected_value = metadata[selected_index]
		info = browser.select(selected_value)
		if player_frame == get_current_screen():
			populate_listbox(listbox, selected_index)
		elif playlist_frame == get_current_screen():
			pass

		if info is not None and not str(selected_value) == str(player.metadata):
			# if selection is an mp3 file and selection isn't the same as the playing audio, then start player
			player_start(selected_index, info)
	except Exception as e:
		print("Couldn't continue:", e)


def handle_back(event):
	# the CANCEL button
	listbox = get_listbox()
	try:
		selected_index = listbox.curselection()[0]
		browser.navigate_cwd_out()
		populate_listbox(listbox, selected_index)
	except Exception as e:
		print("Couldn't continue:", e)

def on_select(event):
	# do stuff when selection changes
	contents = browser.get_items_in_directory(browser.cwd)
	selected_index = listbox_main.curselection()[0]
	selected_value = listbox_main.get(selected_index)

def select_move_up(event):
	listbox = get_listbox()
	try:
		selected_index = listbox_main.curselection()[0]
		if selected_index != 0:
			listbox.selection_clear(first=selected_index, last=selected_index)
			change_selection(listbox, selected_index - 1)
	except Exception as e:
		print("Couldn't move selection up:", e)

def select_move_down(event):
	listbox = get_listbox()
	try:
		selected_index = listbox_main.curselection()[0]
		if selected_index != len(listbox_main.get(0, "end")) - 1:
			listbox.selection_clear(first=selected_index, last=selected_index)
			change_selection(listbox, selected_index + 1)
	except Exception as e:
		print("Couldn't move selection down:", e)
	



def change_selection(listbox, selection):
	listbox.selection_set(selection)
	listbox.activate(selection)
	listbox.focus_set()
	listbox.see(selection)

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
	('d', 's'): player_next,
	('a', 's'): player_prev,
	('s',): player_pause,
	('a',): player_rw,
	('d',): player_ff,
	('e',): handle_enter,
	('w',): handle_back,
	('r',): select_move_up,
	('f',): select_move_down,
	('q',): swap_screen,
	('Prior',): player_volume_up,
	('Next',): player_volume_down,
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

change_screen(player_frame)
populate_listbox(listbox_main, 0)
radio_graphics_loop()
stopwatch_loop()
root.mainloop()