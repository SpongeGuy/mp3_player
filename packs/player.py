import pygame
import sys
import os
import packs.browser as browser
import threading
import time

pygame.init()
pygame.mixer.init()

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

class MusicPlayer:
	def __init__(self, playlist):
		self.playlist = playlist
		self.index = 0
		self.playing = False
		self.paused = True
		self.elapsed_time = 0
		self.length = 999999
		self._duration_loop()
		self._song_end_loop()

	def _duration_loop(self):
		def loop():
			while True:
				self.elapsed_time += 0.25
				time.sleep(0.25)
		threading.Thread(target=loop, daemon=True).start()

	def _song_end_loop(self):
		def loop():
			while True:
				if self.elapsed_time > self.length:
					print("song end")
					self.next_song()
				time.sleep(0.1)
		threading.Thread(target=loop, daemon=True).start()

	def _update_song_length(self):
		self.length = pygame.mixer.Sound(self.playlist[self.index]).get_length()

	def load_song(self):
		pygame.mixer.music.load(self.playlist[self.index])

	def play(self):
		if not self.playing:
			self.elapsed_time = 0
			self.load_song()
			self._update_song_length()
			pygame.mixer.music.play()
			self.playing = True
			self.paused = False
			print("playing")

	def pause(self):
		pygame.mixer.music.pause()
		self.paused = True
		print("paused")
			

	def resume(self):
		pygame.mixer.music.unpause()
		self.paused = False
		print("resumed")

	def stop(self):
		pygame.mixer.music.stop()
		self.playing = False
		print("stopped")

	def next_song(self):
		try:
			self.stop()
			self.index = (self.index + 1) % len(self.playlist)
			self.play()
			print("next")
		except Exception as e:
			print("Could not skip to next song:", e)

	def previous_song(self):
		# skip to beginning of song if elapsed time > 2
		if self.elapsed_time > 2:
			self.elapsed_time = 0
			pygame.mixer.music.set_pos(self.elapsed_time)
			print("beginning")
			return
		# else skip to previous song
		try:
			self.stop()
			self.index = (self.index - 1) % len(self.playlist)
			self.play()
			print("previous")
		except Exception as e:
			print("Could not skip to previous song:", e)

	def fast_forward(self, seconds=0.2):
		self.elapsed_time += seconds
		print("ff", self.elapsed_time)
		pygame.mixer.music.set_pos(self.elapsed_time)


	def rewind(self, seconds=1):
		seconds = self.elapsed_time / 80 + 0.2
		if self.elapsed_time - seconds >= 0:
			self.elapsed_time -= seconds
		print("rw", self.elapsed_time)
		pygame.mixer.music.set_pos(self.elapsed_time)
		

cwd = "C:\\source\\repos\\python\\mp3_player\\music\\Disasterpeace\\FEZ"
browser.cwd = cwd
contents = browser.get_directories(cwd)
playlist = []
for item in contents:
	if isinstance(item, tuple):
		playlist.append(browser.get_song_filepath(item))


player = MusicPlayer(playlist)

def space_key(event):
	if not player.playing:
		player.play()
	elif player.playing and not player.paused:
		player.pause()
	elif player.playing and player.paused:
		player.resume()

def right_key(event):
	player.fast_forward()

def left_key(event):
	player.rewind()

def j_key(event):
	player.previous_song()

def k_key(event):
	player.next_song()

import tkinter as tk

root = tk.Tk()
root.bind('<space>', space_key)
root.bind('<Right>', right_key)
root.bind('<Left>', left_key)
root.bind('<k>', k_key)
root.bind('<j>', j_key)

root.mainloop()