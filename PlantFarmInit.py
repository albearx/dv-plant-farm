import curses
import os
import pyautogui
import time
from termcolor import colored

script_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_path)

# log = open('./PlantFarmLog.txt', 'w')

# Preconditions: Breeding cave and nursery are on the same screen when completely
# zoomed in with either selected.
# Nursery has a plant dragon egg in any nursery slot.
# Breeding cave is currently selected and empty, with the prior breed being two plant dragons.
# 
# Step 1: If retry breed button is present, click it
# Step 2: If breed button is present, click it
# Step 3: Use image hashing to select the nursery
# Step 4: If plant egg on left is present with NO TIMER, click it
# Step 5: If sell button is present, click it
# Step 6: If yes button is present, click it
# Step 7: If heart is over breeding cave, click it
# Step 8: If "Place in Nursery" button is present, click it
# Step 9: Use image hashing to reselect the breeding cave

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

execute = True
img_directory = './PlantFarmImgs'
iteration = 1
time_str = '0s'
total_runtime = 0
start = None
reset_count = -1

# Assumes the view of park includes both the nursery and the cave
# Sets preconditions for plant_farm()
def set_preconditions():
  # log.write('Setting plant farm precondition...\n')
  global stdscr
  attempts = 0
  nursery_has_egg = False
  breed_complete = False
  stdscr.clear()
  stdscr.addstr(0, 0, 'Checking for plant egg in nursery...', curses.color_pair(3))
  stdscr.refresh()

  while nursery_has_egg is False and attempts < 10:
    if pyautogui.locateOnScreen(img_directory + '/nursery.png', confidence = 0.9) is not None:
      stdscr.clear()
      stdscr.addstr(0, 0, 'Nursery has plant egg', curses.color_pair(3))
      stdscr.refresh()
      nursery_has_egg = True
    attempts += 1
  if nursery_has_egg is False:
    stdscr.clear()
    stdscr.addstr(0, 0, 'Nursery does not have plant egg', curses.color_pair(3))
    stdscr.refresh()

  attempts = 0
  stdscr.clear()
  stdscr.addstr(1, 0, 'Checking if cave is occupied...', curses.color_pair(3))
  stdscr.refresh()
  while breed_complete is False and attempts < 10:
    if pyautogui.locateOnScreen(img_directory + '/breed_heart.png', confidence = 0.93) is not None:
      stdscr.clear()
      stdscr.addstr(1, 0, 'Cave is occupied', curses.color_pair(3))
      stdscr.refresh()
      breed_complete = True
    attempts += 1
  if breed_complete is False:
    stdscr.clear()
    stdscr.addstr(1, 0, 'Cave is not occupied', curses.color_pair(3))
    stdscr.refresh()

  if (nursery_has_egg and breed_complete):
    # log.write('Precondition scenario: nursery has egg and breeding cave is occupied.\n')
    stdscr.clear()
    stdscr.addstr(0, 0, 'Set Preconditions Case 1', curses.color_pair(3))
    stdscr.refresh()
    find_and_click(img_directory + '/nursery.png', 0.9, 'Nursery')
    find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
    find_and_click(img_directory + '/sell_button.png', 0.9, 'Sell Button')
    find_and_click(img_directory + '/yes_button.png', 0.9, 'Yes Button')
    find_and_click(img_directory + '/breed_heart.png', 0.9, 'Breed Complete')
    find_and_click(img_directory + '/place_in_nursery.png', 0.9, 'Place in Nursery')
    find_and_click(img_directory + '/breeding_cave.png', 0.9, 'Reselect Breeding Cave')
  elif nursery_has_egg:
    # log.write('Precondition scenario: nursery has egg and breeding cave is NOT occupied.\n')
    stdscr.clear()
    stdscr.addstr(0, 0, 'Set Preconditions Case 2', curses.color_pair(3))
    stdscr.refresh()
    find_and_click(img_directory + '/breeding_cave.png', 0.9, 'Reselect Breeding Cave')
  elif breed_complete:
    # log.write('Precondition scenario: nursery does NOT have egg and breeding cave is occupied.\n')
    stdscr.clear()
    stdscr.addstr(0, 0, 'Set Preconditions Case 3', curses.color_pair(3))
    stdscr.refresh()
    find_and_click(img_directory + '/breed_heart.png', 0.9, 'Breed Complete')
    find_and_click(img_directory + '/place_in_nursery.png', 0.9, 'Place in Nursery')
    find_and_click(img_directory + '/breeding_cave.png', 0.9, 'Reselect Breeding Cave')
  else:
    # log.write('Precondition scenario: nursery does NOT egg and breeding cave is NOT occupied.\n')
    stdscr.clear()
    stdscr.addstr(0, 0, 'Set Preconditions Case 4', curses.color_pair(3))
    stdscr.refresh()
    find_and_click(img_directory + '/breeding_cave.png', 0.9, 'Reselect Breeding Cave')
    find_and_click(img_directory + '/breed_retry_button.png', 0.9, 'Retry Breed Button')
    find_and_click(img_directory + '/breed_button.png', 0.9, 'Breed Button')
    find_and_click(img_directory + '/breed_heart.png', 0.9, 'Breed Complete')
    find_and_click(img_directory + '/place_in_nursery.png', 0.9, 'Place in Nursery')
    find_and_click(img_directory + '/breeding_cave.png', 0.9, 'Reselect Breeding Cave')

# In the event of a game crash, relaunch the game and restart plant farm
def reset_game():
  # log.write('[!!!] Game is resetting.\n')
  global stdscr
  restart_time = 5
  # Crash due to other device connecting (give more time)
  if pyautogui.locateOnScreen(img_directory + '/continue.png', confidence=0.9) is not None:
    restart_time = 300
  # Crash otherwise (shorter time till restart)
  for x in range(restart_time, 0, -1):
    stdscr.clear()
    stdscr.addstr('(Re)starting plant farm in %d seconds...' % x, curses.color_pair(5))
    stdscr.refresh()
    time.sleep(1)

  global reset_count
  reset_count += 1

  
  stdscr.clear()
  stdscr.addstr('Tapping recent apps', curses.color_pair(5))
  stdscr.refresh()
  # log.write('Tapping \"Recent Apps\"...\n')
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/recent_apps.png')))
  time.sleep(1)

  stdscr.clear()
  stdscr.addstr('Clearing recent apps', curses.color_pair(5))
  stdscr.refresh()
  # log.write('Tapping \"Clear All\"...\n')
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/clear_all.png')))
  time.sleep(1)

  stdscr.clear()
  stdscr.addstr('Relaunching', curses.color_pair(5))
  stdscr.refresh()
  # log.write('Tapping DV App...\n')
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/dv_app.png')))

  # log.write('Waiting for loading screen...\n')
  load_count = 0
  while (pyautogui.locateOnScreen(img_directory + '/goals_grey.png', confidence=0.95) is None and
          pyautogui.locateOnScreen(img_directory + '/goals.png', confidence=0.95) is None):
    load_count += 1
    time.sleep(3)
    if (load_count >= 60):
      reset_game()
  time.sleep(2)

  # log.write('Loading screen completion detected.\n')
  # If there is a pop-up upon loading into the game
  while pyautogui.locateOnScreen(img_directory + '/goals_grey.png', confidence=0.9999) is not None:
    # log.write('Exiting a pop-up.\n')
    stdscr.clear()
    stdscr.addstr('Exiting Pop Ups', curses.color_pair(5))
    stdscr.refresh()
    pyautogui.press('esc')
    time.sleep(2)
  

  stdscr.clear()
  stdscr.addstr('Moving view window to nursery area', curses.color_pair(5))
  stdscr.refresh()
  # log.write('Running Bluestacks macro to move view window to nursery.\n')
  # pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/macro_manager.png')))
  # time.sleep(1)
  # pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/play_macro.png')))
  # time.sleep(19) # should be at least the length of the macro used to move the view window

  find_and_click(img_directory + '/dragonarium.png', 0.95, 'Dragonarium')
  time.sleep(0.5)
  find_and_click(img_directory + '/dragonarium_all.png', 0.95, 'Dragonarium All')
  time.sleep(0.5)
  find_and_click(img_directory + '/dragonarium_wishlist.png', 0.95, 'Dragonarium Wishlist')
  time.sleep(0.5)
  find_and_click(img_directory + '/gaia.png', 0.95, 'Gaia')
  time.sleep(0.5)
  find_and_click(img_directory + '/find_1.png', 0.95, 'First Find')
  time.sleep(0.5)
  find_and_click(img_directory + '/find_2.png', 0.95, 'Second Find')
  time.sleep(1.5)

  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/macro_manager.png')))
  time.sleep(1)
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/play_macro.png')))
  time.sleep(6)
  
  # At this point, the nursery window should be in view.
  # 10 attempts given to find the breeding cave; if breeding cave is not found then game condition is unfixable and terminate
  attempts = 0
  can_see_cave = False
  while (can_see_cave is False and attempts < 10):
    if (pyautogui.locateOnScreen(img_directory + '/breeding_cave.png', confidence=0.95) is not None):
      can_see_cave = True
    attempts += 1
    # log.write('Breeding cave found; macro successful.\n')
  
  if can_see_cave is False:
    # log.write('Breeding cave NOT found; macro unsuccessful.\n')
    raise Exception

  # Set preconditions and restart farm
  set_preconditions()
  plant_farm()

# Given an image path, find and click
def find_and_click(image_path, conf, step):
  # log.write('Attempting to find and click %s...\n' % step)
  success = False
  fail_count = 0
  fail_limit = 20
  if step == 'Breed Complete':
    fail_limit = 125
  
  while (not success):

    if (fail_count >= fail_limit):
      stdscr.move(8, 0)
      stdscr.clrtoeol()
      stdscr.addstr(8, 0, 'Too many consecutive fails, attempting to reset game', curses.color_pair(5))
      stdscr.refresh()
      # log.write('Fail limit reached for this find_and_click() call.\n')
      reset_game()

    loc = pyautogui.locateOnScreen(image_path, confidence = conf)

    if loc is not None:

      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      success = True
      # log.write('%s found.\n' % step)
      stdscr.move(8, 0)
      stdscr.clrtoeol()
      stdscr.addstr(8, 0, 'Executing %s in iteration %d' % (step, iteration), curses.color_pair(2))
      stdscr.refresh()

    else:
      
      # Case where the Nursery HUD dips at the exact moment of click and the program clicks bottom left
      if (step == 'Hatch Plant Egg' and fail_count > 1):
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.addstr(8, 0, 'Avoided critical miss in iteration %d' % iteration, curses.color_pair(2))
        stdscr.refresh()
        # log.write('Hatch Plant Egg NOT found; attempting to backtrack by finding and clicking Nursery.\n')
        find_and_click(img_directory + '/nursery.png', 0.9, 'Nursery')
        find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
        success = True

      if (step == 'Sell Button' and fail_count > 2):
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.addstr(8, 0, 'Avoided critical miss in iteration %d' % iteration, curses.color_pair(2))
        stdscr.refresh()
        # log.write('Sell button NOT found; attempting to backtrack by finding and clicking Nursery.\n')
        find_and_click(img_directory + '/nursery.png', 0.9, 'Nursery')
        find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
        find_and_click(img_directory + '/sell_button.png', 0.95, 'Sell Button')
        success = True

      if (step == 'Dragonarium All' and fail_count > 2):
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.addstr(8, 0, 'Avoided critical miss in step %s' % step, curses.color_pair(2))
        stdscr.refresh()

        find_and_click(img_directory + '/dragonarium.png', 0.9, 'Dragonarium')
        find_and_click(img_directory + '/dragonarium_all.png', 0.9, 'Dragonarium All')
        success = True

      fail_count += 1
      stdscr.move(8, 0)
      stdscr.clrtoeol()
      stdscr.addstr(8, 0, '%s not found in iteration %d, trying again. Attempting game reset in %d more tries.' % (step, iteration, fail_limit - fail_count), curses.color_pair(1))
      stdscr.refresh()
      # log.write('Did not find %s.\n' % step)
    sleep_time = 0.37
    if step == 'Nursery':
      sleep_time += 1
    if step == 'Hatch Plant Egg':
      sleep_time += 0.1 - 0.05
    if step == 'Place in Nursery':
      sleep_time += 0.2 
    if step == 'Reselect Breeding Cave':
      sleep_time += 0.2
    time.sleep(sleep_time)


def plant_farm():
  global iteration
  global time_str
  global total_runtime
  global start
  global reset_count
  global execute
  if (start is None):
    start = time.time()
  
  stdscr.clear()
  stdscr.addstr(0, 0, 'Total EC: - (- on double days)', curses.color_pair(4))
  stdscr.addstr(1, 0, '- iterations completed in -', curses.color_pair(4))
  stdscr.addstr(2, 0, 'Previous iteration duration: -', curses.color_pair(4))
  stdscr.addstr(3, 0, 'Average iteration duration: -', curses.color_pair(4))
  stdscr.addstr(4, 0, 'Average rate: - EC/min (- EC/min on double days)', curses.color_pair(4))
  stdscr.addstr(5, 0, 'Hourly rate: - EC/hr (- EC/hr on double days)', curses.color_pair(4))
  stdscr.addstr(6, 0, 'Reset count: -', curses.color_pair(4))
  stdscr.addstr(7, 0, '========================================================', curses.color_pair(4))
  stdscr.refresh()

  while execute:
		
    iteration_start = time.time()
		# Step 1: If retry breed button is present, click it
    find_and_click(img_directory + '/breed_retry_button.png', 0.9, 'Retry Breed Button')
    
		# Step 2: If breed button is present, click it
    find_and_click(img_directory + '/breed_button.png', 0.9, 'Breed Button')

		# Step 3: Use image hashing to select the nursery
    find_and_click(img_directory + '/nursery.png', 0.9, 'Nursery')

		# Step 4: If plant egg on left is present with NO TIMER, click it
    find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')

		# Step 5: If sell button is present, click it
    find_and_click(img_directory + '/sell_button.png', 0.9, 'Sell Button')
    
		# Step 6: If yes button is present, click it
    find_and_click(img_directory + '/yes_button.png', 0.9, 'Yes Button')

		# Step 7: If heart is over breeding cave, click it
    find_and_click(img_directory + '/breed_heart.png', 0.9, 'Breed Complete')

		# Step 8: If "Place in Nursery" button is present, click it
    find_and_click(img_directory + '/place_in_nursery.png', 0.9, 'Place in Nursery')

		# Step 9: Use image hashing to reselect the breeding cave
    find_and_click(img_directory + '/breeding_cave.png', 0.9, 'Reselect Breeding Cave')

    iteration_end = time.time()
    total_runtime = time.time() - start
    time_str = time.strftime("%H:%M:%S", time.gmtime(total_runtime))

    for i in range(5):
      stdscr.move(i, 0)
      stdscr.clrtoeol()

    stdscr.addstr(0, 0, 'Total EC: %d (%d on double days)' % (iteration * 3, iteration * 6), curses.color_pair(4))
    stdscr.addstr(1, 0, '%d iterations completed in %s' % (iteration, time_str), curses.color_pair(4))
    stdscr.addstr(2, 0, 'Previous iteration duration: %.2fs' % (iteration_end - iteration_start), curses.color_pair(4))
    stdscr.addstr(3, 0, 'Average iteration duration: %.2fs' % (float(total_runtime) / iteration), curses.color_pair(4))
    stdscr.addstr(4, 0, 'Average rate: %.1f EC/min (%.1f EC/min on double days)' % (float(iteration * 3) / (total_runtime / 60), float(iteration * 6) / (total_runtime / 60)), curses.color_pair(4))
    stdscr.addstr(5, 0, 'Hourly rate: %.1f EC/hr (%.1f EC/hr on double days)' % (float(iteration * 3) / (total_runtime / 3600), float(iteration * 6) / (total_runtime / 3600)), curses.color_pair(4))
    stdscr.addstr(6, 0, 'Reset count: %d' % reset_count, curses.color_pair(4))
    stdscr.addstr(7, 0, '========================================================', curses.color_pair(4))

    stdscr.refresh()

    iteration += 1


# Main script

def start_farm():
  for x in range(3, 0, -1):
    stdscr.clear()
    stdscr.addstr('Starting plant farm in %d seconds...' % x, curses.color_pair(5))
    stdscr.refresh()
    time.sleep(1)

  stdscr.clear()
  stdscr.addstr('Initializing plant farm...')
  stdscr.refresh()
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/start_instance.png', confidence=0.99)))
  while (pyautogui.locateOnScreen(img_directory + '/dv_app.png', confidence=0.95) is None):
    time.sleep(2)

  try:
    reset_game()
    stdscr.clear()
    stdscr.addstr('Preconditions set, beginning plant farm', curses.color_pair(3))
    stdscr.refresh()
    plant_farm()
  except Exception as e:
    print(str(e))
    print(colored('Earned a total of %d EC (%d EC on double days) in %s' % (iteration * 3, iteration * 6, time_str), 'cyan'))
    print(colored('Plant Farm Terminated', 'magenta'))

    # log.close()
    curses.endwin()
    

start_farm()
# log.close()
curses.endwin()
