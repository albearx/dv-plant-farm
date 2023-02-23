## Instructions

# Initial setup
After cloning (and ensuring python and pip are installed):

`pip install pyautogui` <br />
`pip install Pillow`  <br />
`pip install opencv-python` <br />
`pip install discord.py` <br />
`pip install colored` <br />

The script itself is in `PlantFarm.py`. All code line numbers refer to within this file.

Install BlueStacks emulator and download Dragonvale on your BlueStacks instance: https://www.bluestacks.com/

IMPORTANT: For the purposes of image hashing, your BlueStacks window that Dragonvale runs on MUST be the same size every time you execute this script. This means that you will have to retake screenshots every time you accidentally resize the window. A way to prevent this is to just have the BlueStacks window at full screen. The image hasher library will not recognize images if they are slightly larger or smaller. In addition, make sure you are zoomed in as much as possible before you take screenshots in order to standardize.

Make sure your breeding cave and nursery are completely visible when zoomed in all the way. This usually means they are adjacent to each other, or close.

Starting from when you first enter the game after the loading screen, record a macro using BlueStacks that moves the view window to where your nursery and breeding cave are. The macro should zoom in completely as well at some point. 

Take the following screenshots and place them in folder which in the same directory as your script. These screenshots must match the given names EXACTLY and be .png filetypes. It is best to cut off the edges for less margin of error. There are 16 required screenshots that you must take from your OWN Dragonvale game on your OWN BlueStacks instance! These are the required names for each of the screenshots and what each of them should look like:

`breed_button.png`: <br />
![breed_button](https://user-images.githubusercontent.com/89762342/220868061-e02931b4-5282-4bd9-9617-5ed0ec435f05.png) <br />
The breed button from the breeding cave.

`breed_heart.png`: <br />
![breed_heart](https://user-images.githubusercontent.com/89762342/220868490-7a0a71ea-0180-489d-b5ac-9b615d90bb26.png) <br />
The breed bubble whenever a breeding cave breed is completed

`breed_retry_button.png`: <br />
![breed_retry_button](https://user-images.githubusercontent.com/89762342/220868629-4d224fd9-58b0-4c07-84a1-37666b156998.png) <br />
The retry breed button that is part of the HUD of a breeding cave

`breeding_cave.png`: <br />
![breeding_cave](https://user-images.githubusercontent.com/89762342/220868726-2d8a1228-9714-4db8-9fc8-409ef766514a.png) <br />
An image of part of the breeding cave. Note that the in-game weather may sometimes cause particles to float in front of the breeding cave, so a smaller picture is preferable that is still able to be distinguished as the breeding cave (i.e. this image is found nowhere else on the screen other than the breeding cave).

`continue.png`: <br />
![continue](https://user-images.githubusercontent.com/89762342/220869001-0effe59b-6f75-40ab-bde9-80ae273010f2.png) <br />
An image of the "continue" button as a part of the error whenever the game loses connection. This error can be replicated by logging onto your park from another device while Dragonvale is running on BlueStacks.

`goals.png`: <br />
![goals](https://user-images.githubusercontent.com/89762342/220869331-09ae31c1-fd6f-450d-a192-63276cdb28a0.png) <br />
An image of the Goals button as part of the in-game HUD. Used to ensure that the park is loaded, as this button is always present in the park.

`goals_grey.png`: <br />
![goals_grey](https://user-images.githubusercontent.com/89762342/220869468-03072a68-5c77-4b05-9304-7f09155f321e.png) <br />
Similar to above, but in the event of a pop up currently occupying the screen.

`hatch_plant_egg.png`: <br />
![hatch_plant_egg](https://user-images.githubusercontent.com/89762342/220869618-a05da3c1-2061-4dc7-83f3-074c92217485.png) <br />
This screenshot can be taken by selecting the nursery, and snipping the middle of the plant dragon egg in the HUD. THIS IS NOT THE IMAGE OF THE EGG IN THE ACTUAL NURSERY.

`macro_manager.png`: <br />
![macro_manager](https://user-images.githubusercontent.com/89762342/220869840-cee744f5-9f65-40ad-a22f-aa87610cc66b.png) <br />
Can be found in the sidebar of the BlueStacks instance. This will allow the program to open up the macro menu.

`nursery.png`: <br />
![nursery](https://user-images.githubusercontent.com/89762342/220869990-0fa513c0-ba41-4cc8-ae82-f97d34077d90.png) <br />
This is a picture of a plant dragon egg in the nursery. THIS IS NOT THE IMAGE OF THE EGG IN THE HUD. If done right, it should look smaller than `hatch_plant_egg.png`.

`ok_button.png`: <br />
![ok_button](https://user-images.githubusercontent.com/89762342/220870211-440bc6f5-3e21-4ffc-ab09-ea78685bd5f5.png) <br />
An image of the OK button. Can be found whenever the nursery is full and you hit the breed complete heart bubble.

`place_in_nursery.png`: <br />
![place_in_nursery](https://user-images.githubusercontent.com/89762342/220870409-1c5993c4-a13f-49ff-89dd-a0b941ed9916.png) <br />
An image of the Place in Nursery button. Can be found by tapping the breed complete bubble with space in the nursery.

`play_macro.png`: <br />
![play_macro](https://user-images.githubusercontent.com/89762342/220870510-094b667e-59aa-43e2-9c4d-eb5ac6ca90f6.png) <br />
Can be found by opening the macro manager from the sidebar of BlueStacks. If you only have one macro, you only need the play button, but I had multiple macros so I included more in the image to distinguish this specific macro with the content on the left. Keep in mind that the script will always try to tap the middle of the given image.

`sell_button.png`: <br />
![sell_button](https://user-images.githubusercontent.com/89762342/220870842-1170a148-a5e0-4b83-8858-3e4b5b6df7ca.png) <br />
Can be found when tapping an egg that has finished incubating in the nursery.

`try_again.png`: <br />
![try_again](https://user-images.githubusercontent.com/89762342/220870904-08904ef8-0bc1-40a4-8598-b8ab75188bca.png) <br />
This screenshot might be difficult to obtain; it only appears when Dragonvale experiences the Lightning Dragon in Server Room error. 

`yes_button.png`: <br />
![yes_button](https://user-images.githubusercontent.com/89762342/220871140-120bcdfe-ddef-4afe-add5-032da3647105.png) <br />
After you click the sell button, this button will appear in the "Are you sure?" pop up.

When all the screenshots have been taken and placed into a folder, in the source code (line 24) enter in the folder with all your screenshots.
