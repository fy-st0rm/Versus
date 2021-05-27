import pygame
import os
import sys

import tkinter as tk
from tkinter.filedialog import *


PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH)
from SpriteSheet import *

# Engines stuff
pygame.init()
root = tk.Tk()
root.withdraw()

# Sizes
win_size = (800, 600)
surface_size = (400, 288)
img_size = (16, 16)
map_size = (int(surface_size[0]/img_size[0]), int(surface_size[1]/img_size[1]))


def load_tiles(path):
	sprite = spritesheet(os.path.join(path))
	tile_imgs = sprite.load_strip([0, 0, img_size[0], img_size[1]], 2)
	
	tiles = {}
	i = 1
	for tile in tile_imgs:
		tiles.update({str(i): tile})
		i += 1

	return tiles


class Map:
	def __init__(self, size):
		self.size = size
		self.map = []
	
	def load_map(self):
		for y in range(self.size[1]):
			column = []
			for x in range(self.size[0]):
				column.append("0")
			self.map.append(column)

	def save(self, game_map, surface):
		path = asksaveasfile()
		
		name = path.name.split("/")
		__name = name[-1]
		name = name[-1].split(".")
		name = name[0]
		name = name + ".png"

		with open(path.name, "w") as s:
			for layer in game_map:
				if "\n" not in layer:
					layer.append("\n")
				s.writelines(layer)
		s.close()

		# saving the img
		n_path = path.name.strip(__name)
		print(n_path)
		os.chdir(n_path)
		pygame.image.save(surface, name)

	def open(self):
		path = askopenfile()
		
		# Reading the text file
		temp_map = []
		with open(path.name, "r") as o:
			temp_map = o.readlines()
		o.close()

		# Adding to the map list
		self.map = []
		for m in temp_map:
			line = []
			for i in m:
				if i != "\n":
					line.append(i)
			self.map.append(line)

	def print_map(self):
		for row in self.map:
			print(row)

class Editor:
	def __init__(self):
		self.loop = True

		self.screen = pygame.display.set_mode(win_size)
		self.surface = pygame.Surface(surface_size)
		
		# Loading the map
		self.map = Map(map_size)
		self.map.load_map()

		# Loading sprites
		self.tiles = load_tiles("../Res/tiles.png")
		self.tiles_key = list(self.tiles.keys())

		self.current_slot = 1
		
		self.spawn_player = False
		self.player_slot = "a"

	def __change_slot(self, event):
		if event.key == pygame.K_LEFT:
			self.spawn_player = False
			if str(self.current_slot - 1) in self.tiles:
				self.current_slot -= 1

		if event.key == pygame.K_RIGHT:
			self.player_spawn = False
			if str(self.current_slot + 1) in self.tiles:
				self.current_slot += 1
		
		if event.key == pygame.K_a:
			self.spawn_player = True
			self.player_slot = "a"

		if event.key == pygame.K_b:
			self.spawn_player = True
			self.player_slot = "b"

	def __event(self):
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				self.loop = False
				quit()
			
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_s:
					self.map.save(self.map.map, self.screen)
				if e.key == pygame.K_o:
					self.map.open()

				self.__change_slot(e)

	def __editing(self):
		# For drawing
		if pygame.mouse.get_pressed()[0]:
			x, y = pygame.mouse.get_pos()
	
			# Scaling the mouse pos
			ratio_x = (win_size[0] / surface_size[0])
			ratio_y = (win_size[1] / surface_size[1])
			x, y = (x / ratio_x, y / ratio_y)
			
			# Dividing by img size to get exact pos in the map
			x, y = int(x/img_size[0]), int(y/img_size[1])
			row, col = y, x
			
			if not self.spawn_player:
				self.map.map[row][col] = str(self.current_slot)
			else:
				self.map.map[row][col] = self.player_slot

		# For removing
		if pygame.mouse.get_pressed()[2]:
			x, y = pygame.mouse.get_pos()
	
			# Scaling the mouse pos
			ratio_x = (win_size[0] / surface_size[0])
			ratio_y = (win_size[1] / surface_size[1])
			x, y = (x / ratio_x, y / ratio_y)
			
			# Dividing by img size to get exact pos in the map
			x, y = int(x/img_size[0]), int(y/img_size[1])
			row, col = y, x
		
			self.map.map[row][col] = "0"

	def __draw(self):
		y = 0
		for row in self.map.map:
			x = 0
			for column in row:
				if column in self.tiles:
					self.surface.blit(self.tiles[column], (x*img_size[0], y*img_size[1]))
				elif column == "a":
					pygame.draw.rect(self.surface, (0, 255, 255), [x*16, y*16, 16, 16])
				elif column == "b":
					pygame.draw.rect(self.surface, (255, 0, 0), [x*16, y*16, 16, 16])
				x += 1
			y += 1
		
	def run(self):
		while self.loop:
			self.surface.fill((0, 0, 0))
		
			self.__event()
			self.__editing()
			self.__draw()

			self.screen.blit(pygame.transform.scale(self.surface, win_size), (0, 0))
			pygame.display.update()


if __name__ == "__main__":
	editor = Editor()
	editor.run()

