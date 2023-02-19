import pyautogui
import time

# Overarching loop for macro.
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

iteration = 1

def find_and_click(image_path, conf, step):

  success = False
  fail_count = 0

  while (not success):

    if (fail_count >= 100):
      print("Too many consecutive fails, terminating at iteration %d" % iteration)
      exit()

    loc = pyautogui.locateOnScreen(image_path, confidence = conf)

    if loc is not None:

      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      # Case where the Nursery HUD sometimes dips at the exact moment of click
      # and the default menu appears
      if (step == 'Hatch Plant Egg'):

        if (pyautogui.locateOnScreen('./WinPCImgs/rift.png', 0.95) is None):
          success = True
        else:
          print('Avoided critical miss in iteration %d' % iteration)
          find_and_click('./WinPCImgs/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail')
          find_and_click('./WinPCImgs/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')

      if (step == 'Hatch Plant Egg (Small)'):

        if (pyautogui.locateOnScreen('./WinPCImgsSmall/rift.png', 0.95) is None):
          success = True
        else:
          print('Avoided critical miss in iteration %d' % iteration)
          find_and_click('./WinPCImgsSmall/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail')
          find_and_click('./WinPCImgsSmall/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')

      success = True
      print('Executing %s in iteration %d' % (step, iteration))

    else:
      
      # Case where the Nursery HUD dips at the exact moment of click and the program clicks bottom left
      if (step == 'Sell Button' and fail_count > 6):
        find_and_click('./WinPCImgs/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail 2')
        find_and_click('./WinPCImgs/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')
        find_and_click('./WinPCImgs/sell_button.png', 0.98, 'Sell Button')
        success = True

      if (step == 'Sell Button (Small)' and fail_count > 6):
        find_and_click('./WinPCImgsSmall/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail 2')
        find_and_click('./WinPCImgsSmall/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')
        find_and_click('./WinPCImgsSmall/sell_button.png', 0.98, 'Sell Button')
        success = True

      fail_count += 1
      print('%s not found in iteration %d, trying again.' % (step, iteration))
    #   time.sleep(0.2)

#   time.sleep(0.2)


def main():
  global iteration
  start = time.time()

  while True: 
		
    iteration_start = time.time()
		# Step 1: If retry breed button is present, click it
    find_and_click('./WinPCImgs/breed_retry_button.png', 0.95, 'Retry Breed Button')
    find_and_click('./WinPCImgsSmall/breed_retry_button.png', 0.95, 'Retry Breed Button')

		# Step 2: If breed button is present, click it
    find_and_click('./WinPCImgs/breed_button.png', 0.95, 'Breed Button')
    find_and_click('./WinPCImgsSmall/breed_button.png', 0.95, 'Breed Button')

		# Step 3: Use image hashing to select the nursery
    find_and_click('./WinPCImgs/nursery.png', 0.93, 'Nursery')
    find_and_click('./WinPCImgsSmall/nursery.png', 0.93, 'Nursery')
		
		# Step 4: If plant egg on left is present with NO TIMER, click it
    find_and_click('./WinPCImgs/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')
    find_and_click('./WinPCImgsSmall/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg (Small)')

		# Step 5: If sell button is present, click it
    find_and_click('./WinPCImgs/sell_button.png', 0.95, 'Sell Button')
    find_and_click('./WinPCImgsSmall/sell_button.png', 0.95, 'Sell Button (Small)')

		# Step 6: If yes button is present, click it
    find_and_click('./WinPCImgs/yes_button.png', 0.95, 'Yes Button')
    find_and_click('./WinPCImgsSmall/yes_button.png', 0.95, 'Yes Button')

		# Step 7: If heart is over breeding cave, click it
    find_and_click('./WinPCImgs/breed_heart.png', 0.9, 'Breed Complete')
    find_and_click('./WinPCImgsSmall/breed_heart.png', 0.95, 'Yes Button')

		# Step 8: If "Place in Nursery" button is present, click it
    find_and_click('./WinPCImgs/place_in_nursery.png', 0.95, 'Place in Nursery')
    find_and_click('./WinPCImgsSmall/place_in_nursery.png', 0.95, 'Place in Nursery')

		# Step 9: Use image hashing to reselect the breeding cave
    find_and_click('./WinPCImgs/breeding_cave.png', 0.95, 'Reselect Breeding Cave')
    find_and_click('./WinPCImgsSmall/breeding_cave.png', 0.95, 'Reselect Breeding Cave')

    iteration_end = time.time()
    total_runtime = time.time() - start
    time_str = time.strftime("%H:%M:%S", time.gmtime(total_runtime))

    print('Finished iteration %d in %.2fs. \nTotal runtime: %s.\nTotal EC: %d (%d on double days)\n=========================' % (iteration, (iteration_end - iteration_start), time_str, iteration * 3, iteration * 6))
    iteration += 1
	#   time.sleep(1)

main()