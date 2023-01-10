import pyautogui
import keyboard

while True:
	keyboard.wait("F14")
	print("You pressed p")

	pyautogui.hotkey('win', '`')
	pyautogui.typewrite("py keylaunch.py", 0)
	pyautogui.press('enter')