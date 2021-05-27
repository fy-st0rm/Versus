import pygame
from pygame import mixer
import time
import os


class Text:
	def __init__(self, font_size, color, surface, text):
		self.font_size = font_size
		self.color = color
		self.surface = surface
		self.text = text

		self.font = pygame.font.SysFont("Consolas", self.font_size)
		self.texture = self.font.render(self.text, True, self.color)
		self.rect = self.texture.get_rect()

	def change_text(self, n_text):
		self.text = n_text
		self.texture = self.font.render(self.text, True, self.color)
		self.rect = self.texture.get_rect()

	def change_color(self, n_color):
		self.color = n_color
		self.texture = self.font.render(self.text, True, self.color)

	def get_rect(self):
		return self.rect

	def set_center(self, point):
		rect = self.texture.get_rect(center=point)
		self.surface.blit(self.texture, rect)

	def draw(self, x, y):
		self.surface.blit(self.texture, (x, y))


class Button:
	def __init__(self, surface, rect, active_color, inactive_color, text, text_color):
		self.surface = surface
		self.rect = rect

		self.active_color = active_color
		self.inactive_color = inactive_color
		self.color = self.inactive_color

		self.text = text
		self.text_color = text_color
		self.font = Text(32, self.text_color, self.surface, self.text)

		self.active = False

	def is_clicked(self, event):
		if self.active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					return True
		return False

	def draw(self):
		mouse = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse):
			self.active = True
			self.color = self.active_color
		else:
			self.active = False
			self.color = self.inactive_color

		pygame.draw.rect(self.surface, self.color, self.rect, 2)
		self.font.change_color(self.color)
		self.font.draw(self.rect.x + (self.rect.width/2 - self.font.get_rect().width/2),
		               self.rect.y + (self.rect.height/2 - self.font.get_rect().height/2))


class Custom_button:
	def __init__(self, surface, rect, active_img, inactive_img):
		self.surface = surface
		self.rect = rect
		self.active_img = active_img
		self.inactive_img = inactive_img

		self.img = self.inactive_img
		self.active = False
		self.play_sound = "ready"

	def __play_sound(self):
		if self.play_sound == "ready":
			self.play_sound = "loading"

			sound = mixer.Sound(os.path.join("../Res/sounds/Mech_0.wav"))
			sound.play()

	def is_clicked(self, e):
		if self.active:
			if e.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					return True
		
		return False

	def draw(self):
		mouse = pygame.mouse.get_pos()
		
		if self.rect.collidepoint(mouse):
			self.active = True
			self.__play_sound()
			self.img = self.active_img
		else:
			self.play_sound = "ready"
			self.active = False
			self.img = self.inactive_img
		
		self.surface.blit(pygame.transform.scale(self.img, (self.rect.w, self.rect.h)), (self.rect.x, self.rect.y))

