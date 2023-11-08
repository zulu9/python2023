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

# evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    print(evdev.categorize(event))
