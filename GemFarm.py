# First parks on each instance:
# Instance 3: DVFarm19
# Instance 4: DVFarm19
# Instance 5: DVFarm19
# Instance 6: DVFarm19
# Instance 7: DVFarm1
# Instance 8: DVFarm1
# Instance 9: DVFarm1
# Instance 10: DVFarm1
# Instance 11: DVFarm1
# Instance 12: DVFarm1
# Instance 13: DVFarm1
# Instance 14: DVFarm10

import curses
import os
import pyautogui
import time
from termcolor import colored

script_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_path)

os.system('color')
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
curses.use_default_colors()

curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

stdscr.keypad(True)
stdscr.nodelay(True)

img_directory = './GemImgs'

def iterate_through_emulator_instance(instance):
  img_path = img_directory + "/cluster" + str(instance)

  # Launch instance through BlueStacks Multi Instance Manager
  loc = pyautogui.locateOnScreen(img_path + "/start_instance.png", confidence = 0.999)
  pyautogui.click(pyautogui.center(loc))

  # Tap on DV app after waiting for instance to launch
  while (pyautogui.locateOnScreen("./WinLaptopImgs" + '/dv_app.png', confidence=0.95) is None):
    time.sleep(2)
  
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen("./WinLaptopImgs/dv_app.png", confidence=0.9)))

  for i in range(21):
    iterate_through_game_instance(i, instance)

  # Original "first" park should be reset as first for next time
  while (pyautogui.locateOnScreen(img_path + '/goals_grey.png', confidence=0.95) is None and
        pyautogui.locateOnScreen(img_path + '/goals.png', confidence=0.95) is None):
    time.sleep(3)
  time.sleep(2)

  find_and_click(img_directory + '/close_instance.png', 0.95, "Close Instance", 20, instance)
  find_and_click(img_directory + '/confirm_close_instance.png', 0.95, "Confirm Close Instance", 20, instance)
  time.sleep(2)


def iterate_through_game_instance(game, instance):
  time.sleep(5)
  img_path = img_directory + "/cluster" + str(instance)
  # Wait until loading bar is finished
  while (pyautogui.locateOnScreen(img_path + '/goals_grey.png', confidence=0.95) is None and
          pyautogui.locateOnScreen(img_path + '/goals.png', confidence=0.95) is None):
    time.sleep(3)
  time.sleep(2)
        
  # Exit pop-ups

  for i in range(3):
    if pyautogui.locateOnScreen(img_path + '/goals_grey.png', confidence=0.9999) is not None:
      stdscr.clear()
      stdscr.addstr('Exiting Pop Ups', curses.color_pair(5))
      stdscr.refresh()
      pyautogui.press('esc')
      time.sleep(2)

  find_and_click(img_directory + "/social.png", 0.9, "Social", game, instance)
  find_and_click(img_directory + "/friends.png", 0.9, "Friends", game, instance)
  find_and_click(img_directory + "/gift.png", 0.96, "Gift", game, instance)
  find_and_click(img_directory + "/social_exit.png", 0.9, "Social Exit", game, instance)
  find_and_click(img_directory + "/options.png", 0.9, "Options", game, instance)
  find_and_click(img_directory + "/switch_park.png", 0.8, "Switch Park", game, instance)
  
  while (pyautogui.locateOnScreen(img_directory + "/view_hidden.png", 0.5) is None):
    time.sleep(2)

  # If last park in the emulator instance, reset park to starting game save
  if (game == 20):
    time.sleep(2)
    pyautogui.click(435, 265)
    time.sleep(1)
    pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + "/yes_button.png", confidence=0.8)))
    return
  # 435, 265 is the location of the second entry in the game list
  j = 0
  for j in range(game):
    pyautogui.moveTo(435, 265)
    pyautogui.drag(0, -68, duration=0.8)
    time.sleep(2)

  if (j == 17):
    pyautogui.click(435, 350)
  elif (j == 18):
    pyautogui.click(435, 415)
  else:
    pyautogui.click(435, 265)
  time.sleep(2)

  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + "/yes_button.png", confidence=0.90)))



def find_and_click(image_path, conf, step, game, instance):
  success = False
  fail_count = 0
  fail_limit = 20
  
  while (not success):

    if (fail_count >= fail_limit):
      # change to throw exception, then catch it to skip the affected instance
      raise Exception("Too many failures in instance %d game %d" % (instance, game))

    loc = pyautogui.locateOnScreen(image_path, confidence = conf)

    if loc is not None:

      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      success = True
      # print(colored('Executing %s in iteration %d' % (step, iteration), 'green'))
      stdscr.move(8, 0)
      stdscr.clrtoeol()
      stdscr.addstr(8, 0, 'Executing %s in game %d in instance %d' % (step, game, instance), curses.color_pair(2))
      stdscr.refresh()

    else:
      
      # Case where the HUD dips at the exact moment of click and the program clicks bottom left
      if (step == "Switch Park" and fail_count > 2):
        # print(colored('Avoided critical miss in iteration %d' % iteration, 'green'))
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.addstr(8, 0, 'Avoided critical miss in game %d' % game, curses.color_pair(2))
        stdscr.refresh()
        find_and_click(img_directory + '/options.png', 0.9, 'Options', game, instance)
        find_and_click(img_directory + '/switch_park.png', 0.9, 'Switch Park', game, instance)

      if (step == "Friends" and fail_count > 2):
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.addstr(8, 0, 'Avoided critical miss in game %d' % game, curses.color_pair(2))
        stdscr.refresh()
        find_and_click(img_directory + '/social.png', 0.9, 'Social', game, instance)
        find_and_click(img_directory + '/friends.png', 0.9, 'Friends', game, instance)

      fail_count += 1
      if (step == 'Gift'):
        time.sleep(1)
        return
      
      
    sleep_time = 1
    time.sleep(sleep_time)

for x in range(3, 0, -1):
  stdscr.clear()
  stdscr.addstr('Starting gem farm in %d seconds...' % x, curses.color_pair(5))
  stdscr.refresh()
  time.sleep(1)

stdscr.clear()

for i in range(9, 15):
  iterate_through_emulator_instance(i)

# iterate_through_emulator_instance(8)
