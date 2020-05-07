# GCodeGenerator
Python tKinter base gcode generator for GRBL based drawing machines

This project is an attempt to learn python

Iniitial commint of python script to generat gcode from images. The srip has basic image manipulation tool as provided by the excellent Pillow library. Tkinter is used to provide the GUI.

This sctipt is used at your own risk as currenly provides no exception handling.

To Use:

1. Open up an image file. File formats such as png etc should work. See Pillow documention for more
2. The image will be displayed on the leeft hand window of the screen.
3. To get an initial converted image press the Convert Image button
4. The goal for the image in the righ hand window would be to get it into a blacke and white format.
5. Play arounf with the settings such as blur et. When you have a good looking image use the binarise checkbox.
6. The binarise checkbock will create a black and white image base on the two sliders
7. The size of the required gcode can be editedt in the Entry boxes
8. Some optimisation values can be added in the other entry boxes
9. When doen press the generate gcode button. After a while a output.nc file will be generated.
10.The default depth is -1mm. The safe travel is 5mm


