oimport pygame
import sys
import os

PATH = os.path.dirname(os.path.abspath(__file__))
print(PATH)
sys.path.insert(0, PATH)

from Player import *
from UI import *


LIGHT_BLUE = (0, 255, 255)
DARK_PURPLE = (32, 20, 41)

current_map = os.path.join("../Res/Maps/map1.txt")   # Current default map for now
buttons = spritesheet(os.path.join("../Res/sprites/buttons.png"))

# Scene manager of the game 
class SceneManager:
	def __init__(self):
		self.scene = None

	def change_scene(self, new_scene):
		self.scene = new_scene

	def run_scene(self):
		if self.scene is not None:
			self.scene.run()
		else:
			print("Scene is: ", self.scene)


class Map:
	def __init__(self, name, img, rect):
		self.img = img
		self.rect = rect
		self.name = name
		
		self.active = False
		self.inactive_col = (0, 0, 0)
		self.active_col = (255, 255, 255)
		self.color = self.inactive_col

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
		x, y = pygame.mouse.get_pos()
		if self.rect.collidepoint(x, y):
			self.active = True
			self.__play_sound()
			self.color = self.active_col
		else:
			self.play_sound = "ready"
			self.active = False
			self.color = self.inactive_col

		screen.blit(pygame.transform.scale(self.img, (self.rect.w, self.rect.h)), (self.rect.x, self.rect.y))
		pygame.draw.rect(screen, self.color, self.rect, 2)


# TODO: Create a map selection pannel 
class MapRoom:
	def __init__(self):
		self.loop = True
		self.map_lst = os.listdir(os.path.join("../Res/Maps"))
		
		self.map_imgs = []
		self.map_names = []

		self.maps = []

		for i in self.map_lst:
			if ".png" in i:
				self.map_imgs.append(pygame.image.load(os.path.join(f"../Res/Maps/{i}")))
			if ".txt" in i:
				self.map_names.append(i)
	
		i = 0
		x = 50
		y = 30
		w = 200
		h = 200

		for img in self.map_imgs:
			self.maps.append(Map(self.map_names[i], img, pygame.Rect(x, y, w, h)))
			i += 1
			x += 250
			if x + w > win_size[0]:
				y += 250
				x = 50

		self.menu_buttons = buttons.load_strip([0, 64, 32, 32], 2)
		self.menu_button = Custom_button(screen, pygame.Rect(50, 500, 100, 100), self.menu_buttons[1], self.menu_buttons[0])

	def _event(self):
		global current_map

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.loop = False
				quit()

			if self.menu_button.is_clicked(event):
				self.loop = False
				menu = MainMenu()
				scene.change_scene(menu)
				scene.run_scene()

			for i in self.maps:
				if i.is_clicked(event):
					current_map = os.path.join(f"../Res/Maps/{i.name}")
					self.loop = False

					game = Game()
					scene.change_scene(game)
					scene.run_scene()

	def __draw_maps(self):
		for i in self.maps:
			i.draw()

	def run(self):
		while self.loop:
			screen.fill(DARK_PURPLE)

			self._event()
			self.__draw_maps()

			self.menu_button.draw()

			pygame.display.update()


class MainMenu:
	def __init__(self):
		self.loop = True

		self.text = Text(80, (0, 0, 0), screen, "Versus")
		#self.play_button = Button(screen, pygame.Rect(win_size[0]/2-300/2, 200, 300, 50), (255, 255, 255), (0, 0, 0), "Play", (0, 0, 0))
		#self.quit_button = Button(screen, pygame.Rect(win_size[0]/2-300/2, 300, 300, 50), (255, 255, 255), (0, 0, 0), "Quit", (0, 0, 0))
		
		self.logo = pygame.image.load(os.path.join("../Res/logo.png"))

		self.play_buttons = buttons.load_strip([0, 0, 32, 32], 2)
		self.play_button = Custom_button(screen, pygame.Rect(win_size[0]/2-100/2, 230, 100, 100), self.play_buttons[1], self.play_buttons[0])
		
		self.quit_buttons =  buttons.load_strip([0, 32, 32, 32], 2)
		self.quit_button = Custom_button(screen, pygame.Rect(win_size[0]/2-100/2, 350, 100, 100), self.quit_buttons[1], self.quit_buttons[0])

	def _event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.loop = False
				quit()

			if self.play_button.is_clicked(event):
				self.loop = False
				map_room = MapRoom()
				scene.change_scene(map_room)
				scene.run_scene()
			
			# Main exit of the game
			if self.quit_button.is_clicked(event):
				self.loop = False
				quit()

	def run(self):
		while self.loop:
			screen.fill(DARK_PURPLE)

			self._event()

			#self.text.draw(win_size[0]/2 - self.text.get_rect().w/2, 70)
			
			screen.blit(self.logo, (win_size[0]/2-self.logo.get_width()/2, 70))
			self.play_button.draw()
			self.quit_button.draw()
			
			clock.tick(60)
			pygame.display.update()


class PauseMenu:
	def __init__(self, game_loop):
		self.loop = True
		self.game_loop = game_loop
		
		self.resume_buttons = buttons.load_strip([0, 0, 32, 32], 2)
		self.resume_button = Custom_button(screen, pygame.Rect(win_size[0]/2-100/2, 200, 100, 100), self.resume_buttons[1], self.resume_buttons[0])

		self.menu_buttons = buttons.load_strip([0, 64, 32, 32], 2)
		self.menu_button = Custom_button(screen, pygame.Rect(win_size[0]/2-100/2, 320, 100, 100), self.menu_buttons[1], self.menu_buttons[0])

	def _event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.loop = False
				quit()

			if self.resume_button.is_clicked(event):
				self.loop = False

			if self.menu_button.is_clicked(event):
				self.loop = False
				self.game_loop.loop = False

				# Changing the scene to the menu
				menu = MainMenu()
				scene.change_scene(menu)

			if self.resume_button.is_clicked(event):
				self.loop = False

			if self.menu_button.is_clicked(event):
				self.loop = False
				self.game_loop.loop = False

				# Changing the scene to the menu
				menu = MainMenu()
				scene.change_scene(menu)
			if self.menu_button.is_clicked(event):
				self.loop = False
				self.game_loop.loop = False

				# Changing the scene to the menu
				menu = MainMenu()
				scene.change_scene(menu)
				scene.run_scene()

	def run(self):
		while self.loop:
			screen.fill(DARK_PURPLE)

			self._event()

			self.resume_button.draw()
			self.menu_button.draw()

			clock.tick(60)
			pygame.display.update()


class Game:
	def __init__(self):
		self.loop = True

		self.tiles = {} # Collector for all the entites
		
		self.players = ["Player 1", "Player 2"]
		
		self.tile = spritesheet(os.path.join("../Res/sprites/tiles.png"))
		self.tile_imgs = {
			"1": self.tile.load_image(0, 0, 16, 16),
			"2": self.tile.load_image(1, 0, 16, 16)
		}
		self.map = self._load_map(current_map)
		self._spawn_player()
		self.ground_name = "ground"

	@staticmethod
	def _load_map(path):
		with open(path, "r") as r:
			map = r.readlines() # Reading the textfile line by line and turning into list

		map_ = []
		for m in map:
			line = []
			for i in m:
				if i != "\n":
					line.append(i) # Converting 2d array from the map
			map_.append(line)
		return map_

	def _events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.loop = False
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					# Calling the pause menu
					pause = PauseMenu(self)
					scene.change_scene(pause)
					scene.run_scene()

			self.player1.events(event)
			self.player2.events(event)

	def _spawn_player(self):		
		# Drawing map
		i = 0
		y = 0
		for row in self.map:
			x = 0
			for column in row:
				if column == "a":
					# Spawn pos of player 1
					self.player1 = Player1(surface, self.players[0], (x*16, y*16-25))
					
				if column == "b":
					# Spawn pos of player 2
					self.player2 = Player2(surface, self.players[1], (x*16, y*16-25))
	
				x += 1
			y+=1

	def _end_screen(self, winner):
		self.loop = False
		
		self.end_screen_loop = True
		winner_text = Text(40, (255, 255, 255), screen, f"{winner} win!!")
		
		self.menu_buttons = buttons.load_strip([0, 64, 32, 32], 2)
		menu_button = Custom_button(screen, pygame.Rect(win_size[0]/2-100/2, win_size[1]/2-100/2, 100, 100), self.menu_buttons[1], self.menu_buttons[0])
		
		while self.end_screen_loop:
			screen.fill(DARK_PURPLE)

			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					self.end_screen_loop = False
					quit()

				if menu_button.is_clicked(e):
					menu = MainMenu()
					scene.change_scene(menu)
					scene.run_scene()

			winner_text.draw(win_size[0]/2 - winner_text.get_rect().w/2, 200)
			menu_button.draw()

			pygame.display.update()

	def run(self):
		while self.loop:
			surface.fill(DARK_PURPLE)

			self._events()

			self.player1.draw(self.tiles, win_size, self.players)
			self.player2.draw(self.tiles, win_size, self.players)

			# Checking for winnner
			if len(self.players) == 1:
				self._end_screen(self.players[0])

			# Drawing map
			i = 0
			y = 0
			for row in self.map:
				x = 0
				for column in row:
					if column in self.tile_imgs:
						#pygame.draw.rect(surface, (255, 0, 0), [x*16, y*16, 16, 16])
						surface.blit(self.tile_imgs[column], (x*16, y*16))

					if column in ["1", "2"]:
						self.tiles.update({self.ground_name+"_"+str(i): pygame.Rect(x*16, y*16, 16, 16)})
						i += 1

					x += 1
				y += 1

			self.player1.draw_health_bar((10, 10), (0, 255, 255))
			self.player2.draw_health_bar((290, 10), (255, 0, 0))

			screen.blit(pygame.transform.scale(surface, win_size), (0, 0))
			clock.tick(60)
			pygame.display.update()


pygame.init()
win_size = (800, 600)
clock = pygame.time.Clock()

screen = pygame.display.set_mode(win_size)

pygame.display.set_caption("Versus")
logo = pygame.image.load(os.path.join("../Res/icon.png"))
pygame.display.set_icon(logo)

surface = pygame.Surface((400, 288))

menu = MainMenu()

scene = SceneManager()
scene.change_scene(menu)
scene.run_scene()
