import pyautogui
from pynput.mouse import Controller
import pynput.mouse

def click_center_screen():
    mouse = Controller()
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width / 2
    center_y = screen_height / 2
    mouse.position = (center_x, center_y)
    mouse.click(pynput.mouse.Button.left, 1)