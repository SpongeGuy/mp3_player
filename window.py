import tkinter as tk
from tkinter import font
from time import strftime
import packs.browser as browser

def color(rgb):
	# translates rgb tuple of int to a tkinter friendly color code
	r, g, b = rgb
	return f'#{r:02x}{g:02x}{b:02x}'

# ============================window============================
window = tk.Tk()
window.title("MP3 Player")
window.geometry("240x280")
window.configure(bg=color((0, 0, 0)))
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=3)
window.resizable(0, 0)

# ============================fonts============================
clock_font = font.Font(family="Digital Display", size=30)
vcr_font = font.Font(family="VCR OSD Mono", size=24)
craft_font = font.Font(family="Crafter's Delight", size=12)
small_craft_font = font.Font(family="Crafter's Delight", size=8)

# ============================clock============================
label_clock = tk.Label(
	window, 
	font=small_craft_font, 
	fg='white', 
	bg='black'
	)
label_clock.grid(row=0, column=1, sticky='e')

def clock_loop(label):
	def loop():
		string = strftime('%H:%M:%S %p')
		label.config(text=string)
		label.after(1000, loop)
	loop()

# ============================stopwatch============================
from time import perf_counter
from datetime import datetime

label_stopwatch = tk.Label(
	window, 
	font=clock_font, 
	fg='white', 
	bg='black',
	text="00:00"
	)
label_stopwatch.grid(row=1, column=0, sticky='w')

start_time = None
running = False

def elapsed_time():
	now = perf_counter()
	elapsed_seconds = int(now - start_time)
	minutes, seconds = divmod(elapsed_seconds, 60)
	formatted_time = "%02d:%02d" % (minutes, seconds)
	return formatted_time

def stopwatch_loop(label):
	def loop():
		global running
		if running:
			string = elapsed_time()
			label.config(text=string)
		label.after(1000, loop)
	loop()

def stopwatch_start():
	global start_time
	global running
	start_time = perf_counter()
	running = True
	stopwatch_loop(label_stopwatch)

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


test = tk.Label(
	window, 
	font=craft_font, 
	fg='white', 
	bg='black', 
	text="TIME"
	)
test.grid(row=0, column=0, sticky='w')

# ============================player============================
import pygame
import threading
from os.path import join

pygame.init()
pygame.mixer.init()

current_song_filepath = None

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

def handle_song_end_loop(filepath):
	def loop():
		print(pygame.mixer.music.get_pos() // 1000)
		print(filepath)
		for event in pygame.event.get():
			if event.type == MUSIC_END:
				print("Song has stopped playing.")
				stopwatch_pause()
				next_song(filepath)
		label_stopwatch.after(1000, loop)
	loop()

def play_song(filepath):
	def _play(filepath):
		global current_song_filepath

		# this is fucked but idk how else to do it
		contents = browser.get_directories(browser.strip_directory(filepath))
		info = browser.get_song_tuple(browser.get_song_from_filepath(filepath), contents)
		print("Playing " + str(info[2]) + " - " + str(info[3][:-4]))

		current_song_filepath = filepath
		pygame.mixer.music.load(filepath)
		stopwatch_reset()
		pygame.mixer.music.play()
		#handle_song_end_loop(filepath)
	threading.Thread(target=_play, args=(filepath,), daemon=True).start()

def pause_song():
	pygame.mixer.music.pause()
	stopwatch_pause()

def resume_song():
	pygame.mixer.music.unpause()
	stopwach_resume()

from time import sleep
SEEK_TIME = 1

def ff_song(event):
	current_pos = pygame.mixer.music.get_pos()
	target_pos = current_pos + SEEK_TIME
	while current_pos < target_pos and pygame.mixer.music.get_busy():
		pygame.mixer.music.set_pos(current_pos)
		current_pos += 0.1
		sleep(0.1)

# DONE:
# figure out how to do these functions without referencing the selection

# get filepath by stripping filename from path.
# contents = get_directories(filepath)
# have index count until filename matches that of one in contents
# loop through contents index +- 1 times
# join filepath with filename from contents
# play(filepath)

def next_song(filepath):
	try:
		path = browser.strip_directory(filepath)
		contents = browser.get_directories(path)
		
		index1 = 0
		for item in contents:
			if browser.get_song_from_filepath(filepath) == item[3]:
				break
			index1 += 1
		index1 += 1 # this is the next function, so this is incremented once
		index2 = 0
		for item in contents:
			if index1 == index2:
				filepath = join(path, item[3])
				break
			else:
				filepath = None
			index2 += 1
		if filepath is None:
			raise Exception("Index out of range.")

		play_song(filepath)

	except Exception as e:
		print("Couldn't skip to next song:", e)

def previous_song(filepath):
	try:
		path = browser.strip_directory(filepath)
		contents = browser.get_directories(path)
		
		index1 = 0
		for item in contents:
			if browser.get_song_from_filepath(filepath) == item[3]:
				break
			index1 += 1
		index1 -= 1 # this is the previous function, so this is incremented once
		index2 = 0
		for item in contents:
			if index1 == index2:
				filepath = join(path, item[3])
				break
			else:
				filepath = None
			index2 += 1
		if filepath is None:
			raise Exception("Index out of range.")

		play_song(filepath)

	except Exception as e:
		print("Couldn't skip to previous song:", e)

# ============================songlist============================
songlist = tk.Listbox(
	window, 
	bg='black', 
	fg='white', 
	font=craft_font, 
	height=8,
	)
songlist.grid(row=len(window.grid_slaves()), column=0, columnspan=2, sticky='w')

def handle_return(event):
	# runs when enter is pressed on songlist
	# select file to open
	selected_index = songlist.curselection()[0]
	selected_value = songlist.get(selected_index)
	info = browser.select(selected_value)
	populate_songlist(songlist, selected_index)

	if info is not None:
		contents = browser.get_directories(browser.cwd)
		file = browser.get_song_tuple(selected_value, contents)
		filepath = browser.get_song_filepath(file)
		play_song(filepath)


def handle_backspace(event):
	# runs when backspace is pressed on songlist
	# navigate cwd out
	selected_index = songlist.curselection()[0]
	browser.navigate_cwd_out()
	populate_songlist(songlist, selected_index)

def on_select(event):
	# do stuff when selection changes
	contents = browser.get_directories(browser.cwd)
	selected_index = songlist.curselection()[0]
	selected_value = songlist.get(selected_index)

# this will need to be changed later
songlist.bind('<Return>', handle_return)
songlist.bind('<BackSpace>', handle_backspace)
songlist.bind('<<ListboxSelect>>', on_select)
songlist.bind('<k>', lambda e: next_song(current_song_filepath))
songlist.bind('<j>', lambda e: previous_song(current_song_filepath))
songlist.bind('<Right>', ff_song)

def change_selection(selection):
	songlist.select_set(selection)
	songlist.activate(selection)
	songlist.focus_set()
	songlist.see(selection)

def populate_songlist(label, selection):
	def populate():
		contents = browser.get_directories(browser.cwd)
		label.delete(0, tk.END)
		i = 0
		for item in contents:
			item = browser.strip_item(item)
			songlist.insert(i, item)
			i += 1
	populate()
	if selection >= songlist.size():
		selection = 0

	change_selection(selection)
	#songlist.event_generate('<<ListboxSelect>>')








button = tk.Button(window, text="Click me!", command=lambda: print("Button clicked!"), font=vcr_font)

populate_songlist(songlist, 0)
clock_loop(label_clock)
stopwatch_loop(label_stopwatch)
window.mainloop()