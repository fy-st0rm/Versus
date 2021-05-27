import os
import sys
import pygame
from pygame import mixer


PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH)

from SpriteSheet import *
import numpy as np


class Animator:
	def load_image(self, images, speed):
		length = len(images)
		speed = speed/10
		data_base = []

		for i in np.arange(0, length, speed):
			data_base.append(images[int(i)])

		return data_base

	def change_state(self, current_state, new_state, frame):
		if current_state != new_state:
			current_state = new_state
			frame = 0
		return current_state, frame


class Entity:
	def __init__(self, image, surface, pos, image_rect, image_amt, name, bullet_color):
		self.surface = surface
		self.pos = pos
		self.name = name
		self.bullet_color = bullet_color

		self.sprite = spritesheet(image)
		self.player_image = self.sprite.load_strip(image_rect, image_amt)
		self.player = self.player_image[0]

		self.rect = pygame.Rect(pos[0], pos[1], image_rect.w, image_rect.h)

		self.airtime = 0
		self.speed = 2
		self.vertical_movement = 0
		self.movement = [0, 0]

		self.side = "right"
		self.left = False
		self.right = False

		self.health = 100
		self.dead = False

		self.bullets = []
		self.b_state = "ready"
		self.bullet_speed = 5
		self.bullet_w = 10
		self.bullet_h = 2
		self.bullet_name = "bullet"
		self.bullet_dmg = 10

		self.start_ticks = pygame.time.get_ticks()

	def _check_for_bullets(self, tiles):
		for i in tiles:
			for bullet in self.bullets:
				rect = pygame.Rect(bullet[1], bullet[2], self.bullet_w, self.bullet_h)
				if "Player" in i:
					if tiles[i].get_rect().colliderect(rect):
						tiles[i].take_damage(self.bullet_dmg)
						self.bullets.remove(bullet)
						
						sound = mixer.Sound(os.path.join("../Res/sounds/hit.wav"))
						sound.play()
				else:
					if tiles[i].colliderect(rect):
						self.bullets.remove(bullet)

	def _check_for_hit(self, tiles):
		hits = []

		for i in tiles:
			if i != self.name:
				if self.rect.colliderect(tiles[i]):
					if "Player" not in i:
						hits.append(tiles[i])
					else:
						hits.append(tiles[i].get_rect())
		return hits

	def _collisions(self, tiles):
		collision_type = {"left": False, "right": False, "up": False, "down": False}

		self.rect.x += self.movement[0]
		hits = self._check_for_hit(tiles)
		for hit in hits:
			if self.movement[0] > 0:
				self.rect.right = hit.left
				collision_type["right"] = True
			if self.movement[0] < 0:
				self.rect.left = hit.right
				collision_type["left"] = True

		self.rect.y += self.movement[1]
		hits = self._check_for_hit(tiles)
		for hit in hits:
			if self.movement[1] > 0:
				self.rect.bottom = hit.top
				collision_type["down"] = True
			if self.movement[1] < 0:
				self.rect.top = hit.bottom
				collision_type["up"] = True

		return collision_type

	def get_rect(self):
		return self.rect

	def draw_health_bar(self, pos, color):
		self.color = color
		if self.health > 0:
			pygame.draw.rect(self.surface, color, [pos[0], pos[1], self.health, 10])
		pygame.draw.rect(self.surface, (0, 0, 0), [pos[0], pos[1], 100, 10], 2)

	def take_damage(self, dmg):
		self.health -= dmg
		if self.health <= 0:
			self.dead = True

	def fire(self):
		if self.b_state == "ready":
			self.b_state = "fire"

			sound = mixer.Sound(os.path.join("../Res/sounds/shoot.wav"))
			sound.play()

			self.start_ticks = pygame.time.get_ticks()

			bullet_x = None
			if self.side == "left":
				bullet_x = (self.rect.x - self.bullet_w) - 2
			if self.side == "right":
				bullet_x = (self.rect.x + self.rect.w) + 2

			bullet_y = self.rect.y + 15
			if bullet_x is not None:
				self.bullets.append([self.side, bullet_x, bullet_y])

	def draw(self, tiles, win_size, players):

		# Movement mechanics
		self.movement = [0, 0]

		if self.left:
			self.movement[0] -= self.speed
			self.player = self.player_image[1]
		if self.right:
			self.movement[0] += self.speed
			self.player = self.player_image[0]

		self.movement[1] += self.vertical_movement
		self.vertical_movement += 0.3
		if self.vertical_movement > 3:
			self.vertical_movement = 3

		collision_type = self._collisions(tiles)
		if collision_type["down"]:
			self.airtime = 0
		else:
			self.airtime += 1

		# Rendering

		# Adding fire rate
		if self.b_state == "fire":
			seconds=(pygame.time.get_ticks()-self.start_ticks)/1000
			if seconds > 0.5:
				self.b_state = "ready"

		# Rendering bullet
		i = 0
		for bullet in self.bullets:
			if bullet[0] == "left":
				bullet[1] -= self.bullet_speed
			if bullet[0] == "right":
				bullet[1] += self.bullet_speed

			if bullet[1] <= 0:
				self.bullets.remove(bullet)
			if bullet[1] >= win_size[0]:
				self.bullets.remove(bullet)

			pygame.draw.rect(self.surface, self.bullet_color, [bullet[1], bullet[2], self.bullet_w, self.bullet_h])

			# tiles.update({self.bullet_name+"_"+str(i): pygame.Rect(bullet[1], bullet[2], self.bullet_w, self.bullet_h)})
			i += 1

		# Checking for bullet collision
		self._check_for_bullets(tiles)

		# Checking if player fall from map
		if self.rect.y > self.surface.get_height() + 100:
			self.take_damage(100)

		# Checking if player is alive
		if not self.dead:
			self.surface.blit(self.player, (self.rect.x, self.rect.y))
			tiles.update({self.name: self})
		else:
			if self.name in tiles:
				tiles.pop(self.name)
			if self.name in players:
				players.remove(self.name)


class Player1(Entity):
	def __init__(self, surface, name,  pos):
		super().__init__(os.path.join("../Res/sprites/robot.png"), surface, pos, pygame.Rect(0, 0, 16, 25), 2, name, (0, 255, 255))

	def events(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				self.left = True
				self.side = "left"
			if event.key == pygame.K_d:
				self.right = True
				self.side = "right"
			if event.key == pygame.K_w:
				if self.airtime < 6:
					self.vertical_movement = -5
			if event.key == pygame.K_LSHIFT:
				self.fire()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a:
				self.left = False
			if event.key == pygame.K_d:
				self.right = False


class Player2(Entity):
	def __init__(self, surface, name,  pos):
		super().__init__(os.path.join("../Res/sprites/robot.png"), surface, pos, pygame.Rect(0, 25, 16, 25), 2, name, (255, 0, 0))

	def events(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.left = True
				self.side = "left"
			if event.key == pygame.K_RIGHT:
				self.right = True
				self.side = "right"
			if event.key == pygame.K_UP:
				if self.airtime < 6:
					self.vertical_movement = -5
			if event.key == pygame.K_RSHIFT:
				self.fire()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				self.left = False
			if event.key == pygame.K_RIGHT:
				self.right = False
