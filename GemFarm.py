# First parks on each instance:
# Instance 3: DVFarm19
# Instance 4: DVFarm19
# Instance 5: DVFarm19
# Instance 6: DVFarm19
# Instance 7: DVFarm1
# Instance 8: DVFarm1
# Instance 9: DVFarm4
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

log = open('./GemFarmLog.txt', 'w')

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
reset_count = 0
gems_gifted = 0
time_str = '0s'
total_runtime = 0
start = time.time()

def iterate_through_emulator_instance(instance):
  img_path = img_directory + "/cluster" + str(instance)

  log.write('Opening instance %d in multi-instance manager\n' % instance)
  # Launch instance through BlueStacks Multi Instance Manager
  loc = pyautogui.locateOnScreen(img_path + "/start_instance.png", confidence = 0.999)
  pyautogui.click(pyautogui.center(loc))

  log.write('Waiting for emulator instance to load...\n')
  # Tap on DV app after waiting for instance to launch
  while (pyautogui.locateOnScreen("./WinLaptopImgs" + '/dv_app.png', confidence=0.95) is None):
    time.sleep(2)
  
  log.write('Clicking on DV app...\n')
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
  log.write('Working through instance %d, game %d\n' % (instance, game))
  time.sleep(5)
  img_path = img_directory + "/cluster" + str(instance)
  # Wait until loading bar is finished
  log.write('Waiting for loading screen in instance %d, game %d\n' % (instance, game))

  load_count = 0
  while (pyautogui.locateOnScreen(img_path + '/goals_grey.png', confidence=0.95) is None and
          pyautogui.locateOnScreen(img_path + '/goals.png', confidence=0.95) is None):
    load_count += 1
    time.sleep(3)
    if (load_count >= 60):
      log.write("Loading bar not progressing in instance %d, game %d, throwing exception\n" % (instance, game))
      raise Exception("Loading bar not progressing in instance %d, game %d" % (instance, game))

  time.sleep(2)
        
  # Exit pop-ups

  while pyautogui.locateOnScreen(img_path + '/goals_grey.png', confidence=0.9999) is not None:
    log.write('Exiting pop up in instance %d, game %d\n' % (instance, game))
    stdscr.move(5, 0)
    stdscr.clrtoeol()
    stdscr.addstr(5, 0, 'Exiting Pop Ups', curses.color_pair(5))
    stdscr.refresh()
    pyautogui.press('esc')
    time.sleep(2)

  find_and_click(img_directory + "/social.png", 0.9, "Social", game, instance)
  find_and_click(img_directory + "/friends.png", 0.9, "Friends", game, instance)
  time.sleep(1.3)
  find_and_click(img_directory + "/gift.png", 0.96, "Gift", game, instance)
  find_and_click(img_directory + "/social_exit.png", 0.9, "Social Exit", game, instance)
  find_and_click(img_directory + "/options.png", 0.9, "Options", game, instance)
  find_and_click(img_directory + "/switch_park.png", 0.8, "Switch Park", game, instance)
  
  stdscr.clear()
  stdscr.addstr(0, 0, 'Total gems: %d' % gems_gifted, curses.color_pair(4))
  stdscr.addstr(1, 0, 'Duration: %s' % time.strftime("%H:%M:%S", time.gmtime(time.time() - start)), curses.color_pair(4))
  stdscr.addstr(2, 0, 'Reset count: %d' % reset_count, curses.color_pair(4))
  stdscr.addstr(3, 0, '========================================================', curses.color_pair(4))
  stdscr.refresh()

  while (pyautogui.locateOnScreen(img_directory + "/view_hidden.png", 0.5) is None):
    time.sleep(2)

  # If last park in the emulator instance, reset park to starting game save
  log.write('Scrolling to next game...\n')
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
      log.write('[!!!] Too many failures in instance %d, game %d\n' % (instance, game))
      raise Exception("Too many failures in instance %d, game %d, throwing exception" % (instance, game))



    loc = pyautogui.locateOnScreen(image_path, confidence = conf)

    if loc is not None:

      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      success = True
      stdscr.move(5, 0)
      stdscr.clrtoeol()
      stdscr.addstr(5, 0, 'Executing %s in instance %d, game %d' % (step, instance, game), curses.color_pair(2))
      stdscr.refresh()
      log.write('%s succeeded in instance %d, game %d\n' % (step, instance, game))

      if (step == 'Gift'):
        global gems_gifted
        gems_gifted += 1

    else:
      
      # Case where the HUD dips at the exact moment of click and the program clicks bottom left
      if (step == "Switch Park" and fail_count > 2):
        stdscr.move(5, 0)
        stdscr.clrtoeol()
        stdscr.addstr(5, 0, 'Avoided critical miss for Options in game %d' % game, curses.color_pair(2))
        stdscr.refresh()
        log.write('%s failed in instance %d, game %d; backtracking to Options\n' % (step, instance, game))
        find_and_click(img_directory + '/options.png', 0.9, 'Options', game, instance)
        find_and_click(img_directory + '/switch_park.png', 0.9, 'Switch Park', game, instance)
        success = True

      if (step == "Friends" and fail_count > 2):
        stdscr.move(5, 0)
        stdscr.clrtoeol()
        stdscr.addstr(5, 0, 'Avoided critical miss for Social in game %d' % game, curses.color_pair(2))
        stdscr.refresh()
        log.write('%s failed in instance %d, game %d; backtracking to Social\n' % (step, instance, game))
        find_and_click(img_directory + '/social.png', 0.9, 'Social', game, instance)
        find_and_click(img_directory + '/friends.png', 0.9, 'Friends', game, instance)
        success = True

      log.write('%s failed in instance %d, game %d\n' % (step, instance, game))
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
stdscr.addstr(0, 0, 'Total gems: -', curses.color_pair(4))
stdscr.addstr(1, 0, 'Duration: -', curses.color_pair(4))
stdscr.addstr(2, 0, 'Reset count: -', curses.color_pair(4))
stdscr.addstr(3, 0, '========================================================', curses.color_pair(4))
stdscr.refresh()

for i in range(3, 15):
  while True:  # Retry loop
    try:
      iterate_through_emulator_instance(i)
      break  # Break out of the loop if no exception is raised
    except Exception as e:
      log.write(str(e) + "\n")
      reset_count += 1
      print("Exception occurred in instance %d: %s" % (i, str(e)))
      # Restart the emulator instance
      img_path = img_directory + "/cluster" + str(i)
      loc = pyautogui.locateOnScreen(img_path + "/start_instance.png", confidence=0.999)
      if loc is not None:
        log.write('Instance crashed, restarting instance\n')
        print("Restarting instance %d..." % i)
        continue  # Retry the iteration
      else:
        log.write('Instance reached unforeseen scenario but did not crash, restarting instance\n')
        find_and_click(img_directory + '/close_instance.png', 0.95, "Close Instance", 20, i)
        find_and_click(img_directory + '/confirm_close_instance.png', 0.95, "Confirm Close Instance", 20, i)
        time.sleep(5)
        print("Restarting instance %d..." % i)
        continue  # Retry the iteration

print("Finished with %d resets" % reset_count)
log.close()