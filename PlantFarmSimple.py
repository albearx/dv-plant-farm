
import pyautogui
import time
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
  while breed_complete is False and attempts < 15:
    if pyautogui.locateOnScreen(img_directory + '/breed_heart.png', confidence = 0.95) is not None:
      print(colored('Cave is occupied', 'yellow'))
      breed_complete = True
    attempts += 1
  if breed_complete is False: print(colored('Cave is not occupied', 'yellow'))

  if (nursery_has_egg and breed_complete):
    print(colored('Set Preconditions Case 1', 'yellow'))
    find_and_click(img_directory + '/nursery.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
    find_and_click(img_directory + '/sell_button.png', 0.95, 'Sell Button')
    find_and_click(img_directory + '/yes_button.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breed_heart.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Set Preconditions')
  elif nursery_has_egg:
    print(colored('Set Preconditions Case 2', 'yellow'))
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Set Preconditions')
  elif breed_complete:
    print(colored('Set Preconditions Case 3', 'yellow'))
    find_and_click(img_directory + '/breed_heart.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Set Preconditions')
  else:
    print(colored('Set Preconditions Case 4', 'yellow'))
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breed_retry_button.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breed_button.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breed_heart.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/place_in_nursery.png', 0.95, 'Set Preconditions')
    find_and_click(img_directory + '/breeding_cave.png', 0.95, 'Set Preconditions')

# Given an image path, find and click
def find_and_click(image_path, conf, step):
  success = False
  fail_count = 0

  while (not success):

    if (fail_count >= 150):
      raise Exception

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
        find_and_click(img_directory + '/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail')
        find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')

      if (step == 'Sell Button' and fail_count > 2):
        print(colored('Avoided critical miss in iteration %d' % iteration, 'green'))
        find_and_click(img_directory + '/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail 2')
        find_and_click(img_directory + '/hatch_plant_egg.png', 0.9, 'Hatch Plant Egg')
        find_and_click(img_directory + '/sell_button.png', 0.98, 'Sell Button')
        success = True

      fail_count += 1
      print(colored('%s not found in iteration %d, trying again. Attempting game reset in %d more tries.' % (step, iteration, 150 - fail_count), 'red'))
    time.sleep(0.5)


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

time.sleep(3)
try:
  set_preconditions()
  print(colored('Preconditions set, beginning plant farm', 'yellow'))
  plant_farm()
except:
  print('Plant Farm Terminated')