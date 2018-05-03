# import the pygame module, so you can use it
import pygame
import os 
import math
import PIL
from PIL import Image


def load_png(name):
	""" Load image and return image object"""
	fullname = os.path.join('', name)
	image = pygame.image.load(fullname)
	if image.get_alpha is None:
		image = image.convert()
	else:
		image = image.convert_alpha()
	return image, image.get_rect()

# Definerer car klassen
class Car(pygame.sprite.Sprite):
	def __init__(self, vector):
		pygame.sprite.Sprite.__init__(self)
		screen = pygame.display.get_surface()
		self.image, self.rect = load_png('car.png')
		self.area = screen.get_rect()
		self.rect.x=30
		self.rect.y=30
		self.angle = 0
		self.spd = 0

	def update(self,command):
		self.spd=command.spd*5 * (0.5-command.rev)*2
		self.angle=self.angle+5*(command.right-command.left)
		self.image_rot = pygame.transform.scale(self.image, (25,54));
		self.image_rot = pygame.transform.rotate(self.image_rot, self.angle+180)
		self.rect = self.image_rot.get_rect(center=self.rect.center)
		newpos = self.calcnewpos(self.rect,self.angle,self.spd)
		self.rect = newpos

	def calcnewpos(self,rect,angle,spd):
		(dx,dy)=(spd*math.sin(angle/180*3.141592),spd*math.cos(angle/180*3.141592))
		return rect.move(dx,dy)
		

class Command():
	def __init__(self):
		self.spd=0
		self.left=0
		self.right=0
		self.rev=0

	def update(self, a, b, c, d):
		self.spd = a
		self.left = b
		self.right = c
		self.rev = d

	def reset(self):
		self.spd = 0
		self.left = 0
		self.right = 0
		self.rev = 0


# define a main function
def main():
     
	# initialize the pygame module
	pygame.init()
	# load and set the logo
	#logo = pygame.image.load("logo32x32.png")
	#pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")
     
	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((320,240))
     
	# define a variable to control the main loop
	running = True

	car=Car((10,10))
	command = Command()
	command.left=0
     
	# main loop
	while running:
		pygame.time.wait(60)
	# event handling, gets all event from the eventqueue
		
		screen.fill(255)
		car.update(command)
		screen.blit(car.image_rot,car.rect)
		pygame.display.update()

		

		for event in pygame.event.get():
			command.reset()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					command.left=1
				if event.key == pygame.K_RIGHT:
					command.right=1
				if event.key == pygame.K_UP:
					command.spd=1
				if event.key == pygame.K_DOWN:
					command.rev=1
	
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
	
		
def testrun(driver, max_steps):
     
	# initialize the pygame module
	pygame.init()
	# load and set the logo
	#logo = pygame.image.load("logo32x32.png")
	#pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")
     
	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((320,240))
     
	# define a variable to control the main loop
	running = True

	car=Car((10,10))
	command = Command()
	command.left=0
	command.reset()
	car.x=320
	car.y=40
	car.angle=30
	step=0     

	score=0

	# main loop
	while running:
		step+=1
		# event handling, gets all event from the eventqueue
		
		screen.fill((255,255,255))
		car.update(command)

		screen.blit(car.image_rot,car.rect)


		pil_string_image=pygame.image.tostring(screen,"RGBA",False)
		pil_image=Image.frombytes("RGBA",(320,240),pil_string_image)

		command=driver.drive(pil_image)
		pygame.display.update()

		
		if step>max_steps:
			running=0

		score=car.rect.left

		for event in pygame.event.get():	
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False

	return score, driver.save()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
