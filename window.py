import tkinter as tk
from tkinter import font
from time import strftime
import browser.browser as browser

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

# ============================clock============================
clock = tk.Label(
	window, 
	font=craft_font, 
	fg='white', 
	bg='black'
	)
clock.grid(row=0, column=1, sticky='e')

def clock_label(label):
	def time():
		string = strftime('%H:%M:%S %p')
		label.config(text=string)
		label.after(1000, time)
	time()

# ============================stopwatch============================
stopwatch = tk.Label(
	window, 
	font=clock_font, 
	fg='white', 
	bg='black'
	)
stopwatch.grid(row=1, column=0, sticky='w')

from datetime import datetime
counter = 0
running = False

def stopwatch_label(label):
	def stopwatch():
		global counter
		if running:
			tt = datetime.fromtimestamp(counter)
			string = tt.strftime('%M:%S')
			label.config(text=string)
			label.after(1000, stopwatch)
			counter += 1
	stopwatch()

def stopwatch_start(label):
	global running
	running = True
	stopwatch_label(label)

def stopwatch_stop(label):
	global running
	running = False

def stopwatch_reset(label):
	global counter
	counter = 0
	label.config(text='0:0:0')



test = tk.Label(
	window, 
	font=craft_font, 
	fg='white', 
	bg='black', 
	text="TIME"
	)
test.grid(row=0, column=0, sticky='w')

# ============================songlist============================
songlist = tk.Listbox(
	window, 
	bg='black', 
	fg='white', 
	font=craft_font, 
	height=8,
	)
songlist.grid(row=3, column=0, columnspan=2, sticky='W')

def handle_return(event):
	# get selected index
	selected_index = songlist.curselection()[0]
	# get the value
	selected_value = songlist.get(selected_index)
	print(selected_value)

def handle_backspace(event):
	browser.navigate_cwd_out(browser.cwd)

# this will need to be changed later
songlist.bind('<Return>', handle_return)
songlist.bind('<BackSpace>', handle_backspace)

songlist.select_set(0)
songlist.focus_set()

def populate_songlist(label):
	def populate():
		cwd = browser.cwd
		contents = browser.get_directories(cwd)
		for item in contents:
			songlist.insert(1, str(item))
	populate()

# ============================stopwatch============================






button = tk.Button(window, text="Click me!", command=lambda: print("Button clicked!"), font=vcr_font)

populate_songlist(songlist)
clock_label(clock)
stopwatch_start(stopwatch)
window.mainloop()