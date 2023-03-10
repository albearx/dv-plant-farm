import config
import discord
import asyncio
import os
import pyautogui
import time

from discord.ext import commands
from termcolor import colored

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

img_directory = './WinLaptopImgs'
iteration = 1
time_str = '0s'
total_runtime = 0
start = time.time()
reset_count = 0

# Assumes the view of park includes both the nursery and the cave
# Sets preconditions for plant_farm()
def set_preconditions():
  attempts = 0
  nursery_has_egg = False
  breed_complete = False

  print(colored('Checking for plant egg in nursery...', 'yellow'))
  while nursery_has_egg is False and attempts < 10:
    if pyautogui.locateOnScreen(img_directory + '/nursery.png', confidence = 0.95) is not None:
      print(colored('Nursery has plant egg', 'yellow'))
      nursery_has_egg = True
    attempts += 1
  if nursery_has_egg is False: print(colored('Nursery does not have plant egg', 'yellow'))

  attempts = 0
  print(colored('Checking if cave is occupied...', 'yellow'))
  while breed_complete is False and attempts < 10:
    if pyautogui.locateOnScreen(img_directory + '/breed_heart.png', confidence = 0.95) is not None:
      print(colored('Cave is occupied', 'yellow'))
      breed_complete = True
    attempts += 1
  if breed_complete is False: print(colored('Cave is not occupied', 'yellow'))

  if (nursery_has_egg and breed_complete):
    print(colored('Set Preconditions Case 1', 'yellow'))
    find_and_click(img_directory + '/nursery.png', 0.95, 'Nursery')
    find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
    find_and_click(img_directory + '/sell_button.png', 0.95, 'Sell Button')
    find_and_click(img_directory + '/yes_button.png', 0.95, 'Yes Button')
    find_and_click(img_directory + '/breed_heart.png', 0.95, 'Breed Complete')
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Place in Nursery')
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Reselect Breeding Cave')
  elif nursery_has_egg:
    print(colored('Set Preconditions Case 2', 'yellow'))
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Reselect Breeding Cave')
  elif breed_complete:
    print(colored('Set Preconditions Case 3', 'yellow'))
    find_and_click(img_directory + '/breed_heart.png', 0.95, 'Breed Complete')
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Place in Nursery')
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Reselect Breeding Cave')
  else:
    print(colored('Set Preconditions Case 4', 'yellow'))
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Reselect Breeding Cave')
    find_and_click(img_directory + '/breed_retry_button.png', 0.95, 'Retry Breed Button')
    find_and_click(img_directory + '/breed_button.png', 0.95, 'Breed Button')
    find_and_click(img_directory + '/breed_heart.png', 0.95, 'Breed Complete')
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Place in Nursery')
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Reselect Breeding Cave')

# In the event of a game crash, relaunch the game and restart plant farm
def reset_game():
  restart_time = 30
  # Crash due to other device connecting (give more time)
  if pyautogui.locateOnScreen(img_directory + '/continue.png') is not None:
    restart_time = 300
  # Crash otherwise (shorter time till restart)
  for i in range(restart_time, 0, -1):
    if i % 10 == 0:
      print(colored('Restarting in %d seconds' % (i), 'magenta'))
      time.sleep(10)
  global reset_count
  reset_count += 1

  print(colored('Tapping recent apps', 'magenta'))
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/recent_apps.png')))
  time.sleep(1)
  print(colored('Clearing recent apps', 'magenta'))
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/clear_all.png')))
  time.sleep(1)
  print(colored('Relaunching game', 'magenta'))
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/dv_app.png')))
  while (pyautogui.locateOnScreen(img_directory + '/goals_grey.png', confidence=0.95) is None and
          pyautogui.locateOnScreen(img_directory + '/goals.png', confidence=0.95) is None):
    time.sleep(3)
  time.sleep(2)

  # If there is a pop-up upon loading into the game
  for i in range(3):
    if pyautogui.locateOnScreen(img_directory + '/goals_grey.png', confidence=0.9999) is not None:
      print(colored('Exiting pop up', 'magenta'))
      pyautogui.press('esc')
      time.sleep(0.7)
  

  print(colored('Moving view window to nursery area', 'magenta'))
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/macro_manager.png')))
  time.sleep(1)
  pyautogui.click(pyautogui.center(pyautogui.locateOnScreen(img_directory + '/play_macro.png')))
  time.sleep(23) # should be at least the length of the macro used to move the view window
    
  
  # At this point, the nursery window should be in view.
  # 10 attempts given to find the breeding cave; if breeding cave is not found then game condition is unfixable and terminate
  attempts = 0
  can_see_cave = False
  while (can_see_cave is False and attempts < 10):
    if (pyautogui.locateOnScreen(img_directory + '/breeding_cave.png', confidence=0.95) is not None):
      can_see_cave = True
    attempts += 1
  
  if can_see_cave is False:
    raise Exception

  # Set preconditions and restart farm
  set_preconditions()
  plant_farm()

# Given an image path, find and click
def find_and_click(image_path, conf, step):
  success = False
  fail_count = 0
  fail_limit = 20
  if step == 'Breed Complete':
    fail_limit = 125
  
  while (not success):

    if (fail_count >= fail_limit):
      print(colored('Too many consecutive fails, attempting to reset game', 'magenta'))
      reset_game()

    loc = pyautogui.locateOnScreen(image_path, confidence = conf)

    if loc is not None:

      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      success = True
      print(colored('Executing %s in iteration %d' % (step, iteration), 'green'))

    else:
      
      # Case where the Nursery HUD dips at the exact moment of click and the program clicks bottom left
      if (step == 'Hatch Plant Egg' and fail_count > 3):
        print(colored('Avoided critical miss in iteration %d' % iteration, 'green'))
        find_and_click(img_directory + '/nursery.png', 0.93, 'Nursery')
        find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')

      if (step == 'Sell Button' and fail_count > 2):
        print(colored('Avoided critical miss in iteration %d' % iteration, 'green'))
        find_and_click(img_directory + '/nursery.png', 0.93, 'Nursery')
        find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
        find_and_click(img_directory + '/sell_button.png', 0.98, 'Sell Button')
        success = True

      fail_count += 1
      print(colored('%s not found in iteration %d, trying again. Attempting game reset in %d more tries.' % (step, iteration, fail_limit - fail_count), 'red'))
    
    sleep_time = 0.4
    if step == 'Nursery':
      sleep_time += 0.6
    if step == 'Hatch Plant Egg':
      sleep_time += 0.1
    # if step == 'Breed Complete':
    #   sleep_time += 0.2
    if step == 'Yes Button':
      sleep_time += 0.3
    if step == 'Reselect Breeding Cave':
      sleep_time += 0.3
    time.sleep(sleep_time)


def plant_farm():
  global iteration
  global time_str
  global total_runtime
  global start
  global reset_count

  while True: 
		
    iteration_start = time.time()
    print(colored('Beginning iteration %d' % iteration, 'cyan'))
		# Step 1: If retry breed button is present, click it
    find_and_click(img_directory + '/breed_retry_button.png', 0.95, 'Retry Breed Button')
    
		# Step 2: If breed button is present, click it
    find_and_click(img_directory + '/breed_button.png', 0.95, 'Breed Button')

		# Step 3: Use image hashing to select the nursery
    find_and_click(img_directory + '/nursery.png', 0.93, 'Nursery')

		# Step 4: If plant egg on left is present with NO TIMER, click it
    find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')

		# Step 5: If sell button is present, click it
    find_and_click(img_directory + '/sell_button.png', 0.95, 'Sell Button')
    
		# Step 6: If yes button is present, click it
    find_and_click(img_directory + '/yes_button.png', 0.95, 'Yes Button')

		# Step 7: If heart is over breeding cave, click it
    find_and_click(img_directory + '/breed_heart.png', 0.9, 'Breed Complete')

		# Step 8: If "Place in Nursery" button is present, click it
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Place in Nursery')

		# Step 9: Use image hashing to reselect the breeding cave
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Reselect Breeding Cave')

    iteration_end = time.time()
    total_runtime = time.time() - start
    time_str = time.strftime("%H:%M:%S", time.gmtime(total_runtime))

    print(colored('Finished iteration %d in %.2fs' % (iteration, (iteration_end - iteration_start)), 'cyan'))
    print(colored('Total runtime: %s.' % time_str, 'cyan'))
    print(colored('Total EC: %d (%d on double days)' % (iteration * 3, iteration * 6), 'cyan'))
    print(colored('Average rate: %.1f EC/min (%.1f EC/min on double days)' % (float(iteration * 3) / (total_runtime / 60), float(iteration * 6) / (total_runtime / 60)), 'cyan'))
    print(colored('Reset count: %d' % reset_count, 'cyan'))
    print(colored('========================================================\n', 'cyan'))
    iteration += 1
    
# intents = discord.Intents.all()
# bot = commands.Bot(command_prefix='Hi Phil, ', intents=intents)

# @bot.event
# async def on_ready():
#   await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Plant Farming Simulator"))
#   channel = bot.get_channel(config.CHANNEL_ID)
#   await channel.send("`Beginning plant farm on Bear's park`")
#   try:
#     set_preconditions()
#     await plant_farm()
#   except:
#     print('Plant Farm terminated')

#   global iteration

#   await channel.send("`Plant farm process terminated after earning %d event currency per park (%d on double days) in %s, with an avg of %d EC/min (%d EC/min on double days).`" % (iteration * 3, iteration * 6, time_str, (iteration * 3) / (total_runtime / 60), (iteration * 6) / (total_runtime / 60)))
#   exit()

# bot.run(config.BOT_TOKEN)

os.system('color')

for x in range(3, 0, -1):
  print(colored('Starting plant farm in %d seconds...' % x, 'magenta'))
  time.sleep(1)

try:
  set_preconditions()
  print(colored('Preconditions set, beginning plant farm', 'yellow'))
  plant_farm()
except:
  print(colored('Plant Farm Terminated', 'magenta'))

