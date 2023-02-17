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
    loc = pyautogui.locateOnScreen(image_path, confidence = conf)
    if loc is not None:
      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      # Case where the Nursery HUD sometimes dips at the exact moment of click
      # and the default menu appears
      if (step == 'Hatch Plant Egg'):
        if (pyautogui.locateOnScreen('./WinLaptopImgs/rift.png', 0.95) is None):
          success = True
        else:
          print('Avoided critical miss in iteration %d' % iteration)
          find_and_click('./WinLaptopImgs/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail')
          find_and_click('./WinLaptopImgs/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')

      
      success = True
      print('Executing %s in iteration %d' % (step, iteration))
    else:
      
      # Case where the Nursery HUD dips at the exact moment of click and the program clicks bottom left
      if (step == 'Sell Button' and fail_count > 6):
        find_and_click('./WinLaptopImgs/nursery.png', 0.93, 'Avoid Nursery HUD Dip Fail 2')
        find_and_click('./WinLaptopImgs/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')
        find_and_click('./WinLaptopImgs/sell_button.png', 0.98, 'Sell Button')
        success = True
      fail_count += 1
      print('%s not found in iteration %d, trying again.' % (step, iteration))
      time.sleep(0.2)

  time.sleep(0.3)

start = time.time()
while True: 
  
  iteration_start = time.time()
  # Step 1: If retry breed button is present, click it
  find_and_click('./WinLaptopImgs/breed_retry_button.png', 0.95, 'Retry Breed Button')

  # Step 2: If breed button is present, click it
  find_and_click('./WinLaptopImgs/breed_button.png', 0.95, 'Breed Button')

  # Step 3: Use image hashing to select the nursery
  find_and_click('./WinLaptopImgs/nursery.png', 0.93, 'Nursery')
  time.sleep(0.5)
  # Step 4: If plant egg on left is present with NO TIMER, click it
  find_and_click('./WinLaptopImgs/hatch_plant_egg.png', 0.98, 'Hatch Plant Egg')

  # Step 5: If sell button is present, click it
  find_and_click('./WinLaptopImgs/sell_button.png', 0.95, 'Sell Button')

  # Step 6: If yes button is present, click it
  find_and_click('./WinLaptopImgs/yes_button.png', 0.95, 'Yes Button')

  # Step 7: If heart is over breeding cave, click it
  find_and_click('./WinLaptopImgs/breed_heart.png', 0.9, 'Breed Complete')

  # Step 8: If "Place in Nursery" button is present, click it
  find_and_click('./WinLaptopImgs/place_in_nursery.png', 0.95, 'Place in Nursery')

  # Step 9: Use image hashing to reselect the breeding cave
  find_and_click('./WinLaptopImgs/breeding_cave.png', 0.95, 'Reselect Breeding Cave')

  iteration_end = time.time()
  total_runtime = time.time() - start
  time_str = time.strftime("%H:%M:%S", time.gmtime(total_runtime))

  print('Finished iteration %d in %.2fs. \nTotal runtime: %s.\n\n=========================' % (iteration, (iteration_end - iteration_start), time_str))
  iteration += 1
  time.sleep(1)

