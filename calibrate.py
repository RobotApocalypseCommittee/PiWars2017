'''Python file for color calibration at the event'''

import colorsys
import json
import time

import cv2

from settings import RESOLUTIONX, RESOLUTIONY, THRESHOLDS
from tank import TANK


def get_main_color(img):
    flags = cv2.KMEANS_RANDOM_CENTERS
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    centers = cv2.kmeans(image, 1, None, criteria, 10, flags)[2]

    return list(centers[0])

def calibrate_spec(color):
    #assert color in THRESHOLDS

    camera = TANK.camera
    raw_capture = PiRGBArray(camera, size=(640, 480))

    # time to be put into place
    time.sleep(3)

    frame = camera.capture(raw_capture, format='rgb')

    image = frame.array

    cropped_bgr = image[RESOLUTIONY//2-10:RESOLUTIONY//2+10, RESOLUTIONX//2-10:RESOLUTIONX//2+10]

    major_color = get_main_color(cropped_bgr)
    print("RGB: " + str(major_color))

    hsv_major_color = list(colorsys.rgb_to_hsv(major_color[0], major_color[1], major_color[2]))
    hsv_major_color[0] = (hsv_major_color[0]*179)
    hsv_major_color[1] = (hsv_major_color[1]*255)

    print("HSV: " + str(hsv_major_color))

    confirmation = input("Does this look okay? [y/N] ")

    if confirmation.lower() == "y":
        min_thresh = [coolio-10 for coolio in hsv_major_color]
        max_thresh = [coolio+10 for coolio in hsv_major_color]

        THRESHOLDS[color] = [min_thresh, max_thresh]

        json.dump(THRESHOLDS, open("thresholds.json", "w"), sort_keys=True, indent=4)

        return True

    return False

def calibrate_all():
    for key in THRESHOLDS:
        confirmation = input("The next color is \"{}\". Press q to go to the next color or anything else to start the 3 sec countdown to take the picture: ")

        if confirmation.lower() == "q":
            continue

        while True:

            ret = calibrate_spec(key)

            if not ret:
                redo_quest = input("You seemed to cancel that image, do you want to take it again? [Y/n] ")

                if redo_quest.lower() == "n":
                    break

            else:
                break

            