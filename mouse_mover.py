import time
from pyautogui import position, press, moveTo, size
from random import randint 
old_pos = position()
widght, height = size()
while True:
    time.sleep(200)
    current_pos = position()
    if current_pos == old_pos:
        x = randint(-10, 10)
        y = randint(-10, 10)
        moveTo(widght // 2 + x , height // 2 + y)
        press('shift')
        old_pos = position() 
    else:
        old_pos = position()