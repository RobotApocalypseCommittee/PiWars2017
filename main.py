
import drive
#import lineTracker
#import rainbow
#import settings
#import tank
#import tools
import controller

control = controller.Controller()
driver = drive.Driver()

while True:
    values = control.get_values()

    leftX = values.get('left_axes')[0]
    leftY = values.get('left_axes')[1]

    driver.turn_motors(0, int(round(leftY, 2)*100))
    driver.turn_motors(1, int(round(leftY, 2)*100))

    
