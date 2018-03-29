import pyautogui

import time


# get position x y
def show_position():
    p = pyautogui.position()
    while True:
        np = pyautogui.position()
        if np != p:
            tp = pyautogui.position()
            print(tp, '   ---->  {}  {}'.format(tp[0]-192, tp[1]-93))
            p = np
        time.sleep(0.1)

# move mouse slowly
# pyautogui.moveTo(100, 500, duration=5, tween=pyautogui.easeInOutQuad)

# click mouse:
# pyautogui.click()

# Press key
# pyautogui.press('esc')

show_position()
