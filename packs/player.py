import pygame
import sys
import os
import threading
import packs.browser as browser
import time

pygame.init()
pygame.mixer.init()

LOOP_TIME = 0.1

class MusicPlayer:
	def __init__(self, playlist):
		# playlist is a list of file paths to mp3s
		self.cwd = None
		self.metadata = None
		self.playlist = playlist
		self.index = 0
		self.playing = False
		self.paused = False
		self.elapsed_time = 0
		self.length = 999999
		self.volume = 0.5
		self._duration_loop()
		self._song_end_loop()
		self._update_volume()
		self.stop()

	def _duration_loop(self):
		def loop():
			while True:
				if self.playing and not self.paused:
					self.elapsed_time += LOOP_TIME
				time.sleep(LOOP_TIME)
		threading.Thread(target=loop, daemon=True).start()

	def _song_end_loop(self):
		def loop():
			while True:
				if self.elapsed_time > self.length:
					#print("song end")
					self.next_song()
				time.sleep(LOOP_TIME)
		threading.Thread(target=loop, daemon=True).start()

	def _update_volume(self):
		if self.volume > 1:
			self.volume = 1
		elif self.volume < 0:
			self.volume = 0
		pygame.mixer.music.set_volume(self.volume)

	def _update_song_metadata(self):
		contents = browser.get_items_in_directory(self.cwd)
		filename = browser.get_song_from_filepath(self.playlist[self.index])
		self.metadata = browser.get_song_tuple(filename, contents)


	def _update_song_length(self):
		self.length = pygame.mixer.Sound(self.playlist[self.index]).get_length()

	def load_song(self):
		pygame.mixer.music.load(self.playlist[self.index])
		self._update_song_length()
		self._update_song_metadata()

	def play(self):
		if not self.playing:
			self.elapsed_time = 0
			self.load_song()
			pygame.mixer.music.play()
			self.playing = True
			self.paused = False
			#print("playing")

	def pause(self):
		pygame.mixer.music.pause()
		self.paused = True
		#print("paused")
			
	def resume(self):
		pygame.mixer.music.unpause()
		self.paused = False
		#print("resumed")

	def stop(self):
		pygame.mixer.music.stop()
		self.playing = False
		#print("stopped")

	def next_song(self):
		try:
			self.stop()
			self.index = (self.index + 1) % len(self.playlist)
			self.play()
			#print("next")
		except Exception as e:
			print("Could not skip to next song:", e)

	def previous_song(self):
		# skip to beginning of song if elapsed time > 2
		if self.elapsed_time > 2:
			self.elapsed_time = 0
			pygame.mixer.music.set_pos(self.elapsed_time)
			#print("beginning")
			return
		# else skip to previous song
		try:
			self.stop()
			self.index = (self.index - 1) % len(self.playlist)
			self.play()
			#print("previous")
		except Exception as e:
			print("Could not skip to previous song:", e)

	def fast_forward(self, seconds=0.2):
		try:
			self.elapsed_time += seconds
			#print("ff", self.elapsed_time)
			pygame.mixer.music.set_pos(self.elapsed_time)
		except Exception as e:
			print("Couldn't fast forward:", e)


	def rewind(self, seconds=1):
		try:
			seconds = self.elapsed_time / 80 + 0.2
			if self.elapsed_time - seconds >= 0:
				self.elapsed_time -= seconds
			#print("rw", self.elapsed_time)
			pygame.mixer.music.set_pos(self.elapsed_time)
		except Exception as e:
			print("Couldn't rewind:", e)

	def volume_down(self, amount=0.05):
		if self.volume >= 0 and self.volume <= 1:
			self.volume -= amount
			self._update_volume()

	def volume_up(self, amount=0.05):
		if self.volume >= 0 and self.volume <= 1:
			self.volume += amount
			self._update_volume()

	def mute(self):
		pygame.mixer.music.set_volume(0)

	def unmute(self):
		self._update_volume()