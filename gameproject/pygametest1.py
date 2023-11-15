# import the pygame module, so you can use it
import pygame
import evdev

# find gamepads
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# for device in devices:
#     print(device.path, device.name, device.phys)

# creates object 'gamepad' to store the data of the first device found
# you can call it whatever you like
gamepad = evdev.InputDevice(devices[0].path)

# prints out device info at start
print(gamepad)

# define a main function
def main():
	# initialize the pygame module
	pygame.init()
	# load and set the logo
	logo = pygame.image.load("logo32x32.png")
	pygame.display.set_icon(logo)
	pygame.display.set_caption("minimal program")

	# create a surface on screen that has the size of 240 x 180
	screen = pygame.display.set_mode((240, 180))

	# define a variable to control the main loop
	running = True

	# main loop
	while running:
		# event handling, gets all event from the event queue
		for event in pygame.event.get():
			# evdev takes care of polling the controller in a loop
			for event in gamepad.read_loop():
				print(evdev.categorize(event))
			# only do something if the event is of type QUIT ---BROKEN when controller is connected!---
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
	# call the main function
	main()
