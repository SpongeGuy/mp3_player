import tkinter as tk
from tkinter import font
from time import strftime
import packs.browser as browser

LOOP_TIME = 100

WINDOW_HEIGHT = 280
WINDOW_LENGTH = 240

COLOR_GREEN = '#00ff00'
COLOR_GREY = '#1f261e'
COLOR_BLACK = '#000000'
COLOR_WHITE = '#ffffff'
COLOR_BLUE = '#2188ff'

def color(rgb):
	# translates rgb tuple of int to a hexcode
	r, g, b = rgb
	return f'#{r:02x}{g:02x}{b:02x}'

# ============================window============================
window = tk.Tk()
window.title("MP3 Player")
window.geometry(str(WINDOW_LENGTH) + "x" + str(WINDOW_HEIGHT))
window.configure(bg=COLOR_BLACK)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=3)
window.resizable(0, 0)

# ============================fonts============================
clock_font = font.Font(family="Digital Display", size=36)
vcr_font = font.Font(family="VCR OSD Mono", size=24)
large_craft_font = font.Font(family="Crafter's Delight", size=16)
craft_font = font.Font(family="Crafter's Delight", size=12)
small_craft_font = font.Font(family="Crafter's Delight", size=10)

# ============================clock============================
label_clock = tk.Label(
	window, 
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

# ============================status bar============================
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
	window, 
	font=small_craft_font, 
	fg=COLOR_WHITE, 
	bg=COLOR_BLACK,
	text="PLAYING"
	)
label_status.grid(row=0, column=0, sticky='w')

def status_loop():
	def loop():
		if player.paused:
			label_status.config(text="PAUSED")
		elif not player.playing:
			label_status.config(text="STOPPED")
		else:
			label_status.config(text="PLAYING")
		label_status.after(LOOP_TIME, loop)
	loop()

label_now_playing = tk.Label(
	window,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='',
	width=WINDOW_LENGTH,
	anchor='w',
	)
label_now_playing.grid(row=3, column=0, sticky='w', columnspan=3)

label_volume = tk.Label(
	window,
	font=small_craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='VOLUME',
	anchor='e'
	)
label_volume.grid(row=0, column=2, sticky='e')

label_volume_number = tk.Label(
	window,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='',
	anchor='e',
	)
label_volume_number.grid(row=1, column=2, sticky='en')

from tkinter import ttk

bar_frame = ttk.Frame(window, width=WINDOW_LENGTH)
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
	window,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text='Directory'
	)
label_playlist.grid(row=5, column=0, sticky='w')

label_length = tk.Label(
	window,
	font=craft_font,
	fg=COLOR_WHITE,
	bg=COLOR_BLACK,
	text=''
	)
label_length.grid(row=5, column=2, sticky='e')

def currently_playing_loop():
	def loop():
		# label_now_playing
		if not player.playing:
			label_now_playing['text'] = "Not playing"
		if player.metadata is not None:
			label_now_playing['text'] = str(player.metadata[2]) + " - " + str(player.metadata[3][:-4])

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
		

		window.after(LOOP_TIME, currently_playing_loop)
	loop()



# ============================stopwatch============================
from time import perf_counter
from datetime import datetime

label_stopwatch = tk.Label(
	window, 
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




# ============================songlist============================
# bullshit
metadata = [] # this is an analogue to the songlist, storing tuples of metadata instead of filenames.

songlist = tk.Listbox(
	window, 
	bg=COLOR_BLACK, 
	fg=COLOR_WHITE,
	selectbackground=COLOR_BLUE,
	font=craft_font, 
	height=8,
	width=WINDOW_LENGTH,
	highlightthickness=0,
	borderwidth=0,
	)
songlist.grid(row=len(window.grid_slaves()), column=0, columnspan=3, sticky='w')

def populate_songlist(selection):
	global playlist
	global metadata
	playlist = []
	def populate():
		global metadata
		# populate graphical list
		contents = browser.get_items_in_directory(browser.cwd)
		metadata = contents
		songlist.delete(0, tk.END)
		i = 0
		for item in contents:
			item = browser.strip_item(item)
			songlist.insert(i, item)
			i += 1

		# populate playlist list list
		for item in contents:
			if isinstance(item, tuple):
				playlist.append(browser.get_song_filepath(item))
	populate()
	if selection >= songlist.size():
		selection = 0

	change_selection(selection)

def handle_return(event):
	global metadata
	# runs when enter is pressed on songlist
	# select file to open
	selected_index = songlist.curselection()[0]
	selected_value = metadata[selected_index]
	info = browser.select(selected_value)
	populate_songlist(selected_index)

	if info is not None and not str(selected_value) == str(player.metadata):
		# if selection is an mp3 file and selection isn't the same as the playing audio, then start player
		player_start(selected_index, info)


def handle_backspace(event):
	# runs when backspace is pressed on songlist
	# navigate cwd out
	selected_index = songlist.curselection()[0]
	browser.navigate_cwd_out()
	populate_songlist(selected_index)

def on_select(event):
	# do stuff when selection changes
	contents = browser.get_items_in_directory(browser.cwd)
	selected_index = songlist.curselection()[0]
	selected_value = songlist.get(selected_index)

# this will need to be changed later
window.bind('<Return>', handle_return)
window.bind('<BackSpace>', handle_backspace)
window.bind('<<ListboxSelect>>', on_select)
window.bind('<space>', player_pause)
window.bind('<Prior>', player_volume_up)
window.bind('<Next>', player_volume_down)
window.bind('<l>', player_ff)
window.bind('<j>', player_rw)

def change_selection(selection):
	songlist.select_set(selection)
	songlist.activate(selection)
	songlist.focus_set()
	songlist.see(selection)








button = tk.Button(window, text="Click me!", command=lambda: print("Button clicked!"), font=vcr_font)

populate_songlist(0)
#clock_loop(label_clock)
status_loop()
currently_playing_loop()
stopwatch_loop()
window.mainloop()