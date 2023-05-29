# Instructions
### (Skip if environment already set up)

Download and install Python: https://www.python.org/downloads/ <br />
Ensure python is installed by opening command prompt after installation is complete by typing python --Version. If the command prompt says something along the lines of "unrecognized command", the installation was unsuccessful. <br /> <br />

Make a new folder in your Desktop. Name it something like "DVPlantFarm". This is where all of your files for this plant farm will go. <br />
In the command prompt, set the working directory to your Desktop. This can usually be done by typing `cd Desktop` in the terminal, but can vary depending on how your PC is set up. Type `cd DVPlantFarm` (or whatever the name of your folder is) to enter the program directory.<br /> <br />

# Initial setup
After cloning (and ensuring python and pip are installed):

`pip install pyautogui` <br />
`pip install Pillow`  <br />
`pip install opencv-python` <br />
`pip install windows-curses` (if you're using Windows)<br />
`pip install termcolor` <br />
`pip install colored` <br />

The script itself is in `PlantFarmInit.py`. This is the only file you really need from this repository.

Install BlueStacks emulator and download Dragonvale on your BlueStacks instance: https://www.bluestacks.com/. Make sure you are using Bluestacks 5 (not X or 10).

Add Gaia to your Dragonarium wishlist. Make sure she is visible on the wishlist without scrolling. The script will use the Dragonarium to revisit your nursery/breeding cave area in the event of a game crash.

Use the Dragonarium to find Gaia. Do not touch anything after the Dragonarium finds Gaia. Afterward, record a Bluestacks macro that zooms all the way into the game, and in the macro manager open the settings of this macro and uncheck the option "Show this window after executing" (or something along those lines). The script will use this macro to zoom into the game. This is crucial for the script to restart the game in the event of a crash.

IMPORTANT: For the purposes of image hashing, your BlueStacks window that Dragonvale runs on MUST be the same size every time you execute this script. This means that you will have to retake screenshots every time you accidentally resize the window. A way to prevent this is to just have the BlueStacks window at full screen. The image hasher library may not recognize images if they are slightly larger or smaller. In addition, make sure you are zoomed in as much as possible before you take screenshots in order to standardize. In addition, make sure your nursery is full and includes at least one plant dragon egg. This is because when less eggs are in the nursery, the buttons get bigger which throws off the image hashing. You can fill your nursery with plant eggs to meet this requirement.

Make sure your breeding cave and nursery are completely visible when zoomed in all the way. This usually means they are adjacent to each other, or close.

In your DVPlantFarm folder, make a new folder called `PlantFarmImgs`. This is where you will put your screenshots. Take the following screenshots and place them in folder which in the same directory as your script. These screenshots must match the given names EXACTLY and be .png filetypes. It is best to cut off the edges for less margin of error. For some of the screenshots, try and take them in areas that do not often have animations. Make sure buildings such as the breeding cave are not selected when you take the screenshot (the "selected" effect where the building glows white may interfere). There are 24 required screenshots that you must take from your OWN Dragonvale game on your OWN BlueStacks instance! Examples and names of the screenshots can be found in the `WinLaptopImgs` folder in this repository. Make sure all of the names match EXACTLY.

To begin your plant farm, open your Bluestacks Multi Instance Manager. Make sure it is in view on your screen. In your command prompt, type `python PlantFarmInit.py` in order to begin the farm. To stop the farm, move your cursor (quickly) to any corner of the screen. 

DM me on Discord `@AACommander#6432` if you need any further assistance/explanation.
