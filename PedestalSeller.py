import curses
import os
import pyautogui
import time

from termcolor import colored


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

img_directory = './WinLaptopImgs'
iteration = 0


# Given an image path, find and click
def find_and_click(image_path, conf, step):
  success = False
  fail_count = 0
  fail_limit = 20
  while (not success):

    if (fail_count >= fail_limit):
      stdscr.move(8, 0)
      stdscr.clrtoeol()
      stdscr.addstr(8, 0, 'Too many consecutive fails, attempting to reset game', curses.color_pair(5))
      stdscr.refresh()
      # print(colored('Too many consecutive fails, attempting to reset game', 'magenta'))
      raise Exception

    loc = pyautogui.locateOnScreen(image_path, confidence = conf)

    if loc is not None:

      target_center = pyautogui.center(loc)
      pyautogui.click(target_center)

      success = True
      stdscr.move(8, 0)
      stdscr.clrtoeol()
      stdscr.addstr(8, 0, 'Executing %s in iteration %d' % (step, iteration), curses.color_pair(2))
      stdscr.refresh()
      time.sleep(0.8)
    else:
      fail_count += 1
      time.sleep(0.3)

def pedestal_farm():
  global iteration
  stdscr.clear()
  stdscr.addstr(0, 0, 'Iterations: -', curses.color_pair(4))
  stdscr.refresh()
  while True: 
		
    # print(colored('Beginning iteration %d' % iteration, 'cyan'))
		# Step 1: If retry breed button is present, click it
    find_and_click(img_directory + '/rosebud_pedestal.png', 0.95, 'Select Pedestal')
    
		# Step 2: If breed button is present, click it
    find_and_click(img_directory + '/sell_pedestal.png', 0.95, 'Sell Pedestal')

		# Step 3: Use image hashing to select the nursery
    find_and_click(img_directory + '/yes_sell_pedestal.png', 0.93, 'Confirm Sell Pedestal')



    stdscr.clear()

    stdscr.addstr(0, 0, 'Iterations: %d' % iteration, curses.color_pair(4))
    
    stdscr.refresh()

    iteration += 1


# Main script


for x in range(3, 0, -1):
  stdscr.clear()
  stdscr.addstr('Starting pedestal farm in %d seconds...' % x, curses.color_pair(5))
  stdscr.refresh()
  time.sleep(1)

try:
  pedestal_farm()
except:
  print(colored('Pedestal Farm Terminated', 'magenta'))
