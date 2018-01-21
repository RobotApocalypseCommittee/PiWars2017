"""main.py
The script which runs. The mainloop. Quite frightening.
"""
import time
import drive
from robot import ROBOT
#from modes import line, manual_drive, maze, rainbow
import settings
import tools
import controller
import leds

control = controller.Controller()

mode_index = 0
modes = ["manual", "line", "rainbow", "maze", "select"]
mode_colours = ["red", "cyan", "orange", "magenta", "white"]
mode = "manual"

selection_mode = False
joy_last_select_time = 0

joy_toggle_delay = 50

while True:
    values = control.get_values()
    

    if values['control_buttons']['Guide'] and joy_last_select_time + joy_toggle_delay < time.time() and not selection_mode:

        selection_mode = not selection_mode
        joy_last_select_time = time.time()

        leds.start_blinking()

    if mode == "selection":
        if values["button_pad"]['A']:
            shift_mode("line")
            
        elif values["button_pad"]['B']:
            shift_mode("rainbow")

        elif values["button_pad"]['Y']:
            shift_mode("maze")

        elif values["button_pad"]['X']:
            shift_mode("manual")
        
        if values["bumpers"][1]:
            mode_index += 1
            if mode_index == len(modes):
                mode_index = 0

        if values["bumpers"][0]:
            mode_index -= 1
            if mode_index == -1:
                mode_index = len(modes)
        
        if values["control_buttons"]["Guide"]:
                shift_mode(modes[mode_index])

    if mode == "line":
	 #       line.update()
    	pass

    if mode == "rainbow":
        pass

    if mode == "maze":
        pass

    if mode == "manual":
        joyX = int(tools.translate(values['left_axes'][0], -1, 1, -255, 255))
        joyY = int(tools.translate(values['left_axes'][1], -1, 1, -255, 255))

        left_speed = joyX + joyY
        right_speed = joyX - joyY

        ROBOT.driver.turn_motors(0,left_speed)
        ROBOT.driver.turn_motors(1, right_speed)

    

def shift_mode(new_mode):
    global mode
    global selection_mode
    
    mode = new_mode
    selection_mode = False
    new_color = mode_colours[modes.index(new_mode)]

    leds.changecolor(new_color)


ROBOT.driver.safe_shutdown()
