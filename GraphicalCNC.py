from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog as fd
from tkinter import Image
from PIL import Image as ImagePIL
from PIL import ImageTk

from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt




image_width = 0
image_height = 0
g_threshold = 0
low_threshold = 0
image_resize_width = 200
image_resize_height = 180
image_to_show =""
edge = ""
progress1 = ""
labelprogress = ""

master = Tk()
c1 = Canvas(master, width=500, height=400, bg='lightgreen')
panel2 = Label(master)

filename = ""

img1 = ""
scale1 = ""

var_blur = IntVar()
var_contour = IntVar()
var_smooth = IntVar()
var_sharpen = IntVar()

var1 = IntVar()
var2 = IntVar()
binarize = IntVar()
scale1_var = IntVar()
scale2_var = IntVar()
x_res = StringVar()
y_res = StringVar()
spacing = StringVar()
remove_short = StringVar()
start_x = 0;
end_x = 0;
start_y = 0;
end_y = 0;

convert_section = 0;


def process_data():
    global filename, master, img1
    print("Filname  to process: " + str(filename))
    img1 = ImagePIL.open(filename)
    img2 = img1.resize((500, 400))
    img2 = ImageTk.PhotoImage(img2)
    panel = Label(master, image=img2, bg='green')
    panel.image = img2
    panel.place(x=50, y=450)


def callback():
    global filename
    name = fd.askopenfilename()
    filename = name
    print(name)
    process_data()


def process_image():
    global master, img1




def binarize_array_section(numpy_array,start_x,start_y,end_x,end_y, low_threshold=50, threshold=100):
    """Binarize a numpy array."""

    #tmp_array = np.array(numpy_array[start_x:end_x, start_y:end_y])
    tmp_array = np.array(numpy_array[start_y:end_y , start_x:end_x])
    print("Converting section..." +str(start_x) + " "+str(start_y) + " "+str(end_x) + " "+str(end_y) + " ")
    print(tmp_array.shape)

    #numpy_array[start_x:end_x, start_y:end_y] = tmp_array

    row,cols = tmp_array.shape

    for j in range(row):
        for i in range(cols):
            if tmp_array[j][i] >= 0 and tmp_array[j][i] < 255:
                tmp_array[j][i] = 255
                print("changing....")


    #numpy_array[start_x:end_x, start_y:end_y] = tmp_array
    numpy_array[start_y:end_y, start_x:end_x] = tmp_array

    return numpy_array


def binarize_array(numpy_array, low_threshold=50, threshold=100):
    """Binarize a numpy array."""
    global var2
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > low_threshold and numpy_array[i][j] <= threshold:
                if var2.get() == 1:
                    numpy_array[i][j] = 255
                else:
                    numpy_array[i][j] = 0

            else:
                if var2.get() == 0:
                    numpy_array[i][j] = 255
                else:
                    numpy_array[i][j] = 0
    return numpy_array



def modify_final():
    global image_to_show,image_width, image_height, panel2, g_threshold, edge, low_threshold, start_x, start_y, end_x, end_y, convert_section
    edge = np.array(edge)
    panel2.destroy()
    if convert_section == 1:
        convert_section = 0;
        edge = binarize_array_section(edge, start_x, start_y, end_x, end_y, low_threshold=int(low_threshold), threshold=int(g_threshold))
        edge = ImagePIL.fromarray(edge)
    image_to_show = ImageTk.PhotoImage(edge)
    panel2 = Label(master, image=image_to_show)
    panel2.image = image_to_show
    panel2.place(x=650, y=450)
    panel2.bind("<Button-1>", mouse_pressed_callback)
    panel2.bind("<ButtonRelease-1>", mouse_released_callback)
    edge.save('Newfile.png')
    #edge.show()


def convert_image():
    global image_to_show,image_width, image_height, panel2, g_threshold, edge, low_threshold, start_x, start_y, end_x, end_y, convert_section
    print(img1.size)
    panel2.destroy()
    img = img1.resize((500, 400))
    grey = img.convert("L")
    image_width, image_height = img.size
    edge = grey;
    if var1.get() == 1:
        edge = edge.filter(ImageFilter.FIND_EDGES)
    if var_blur.get() == 1:
        edge = edge.filter(ImageFilter.BLUR)
    if var_contour.get() == 1:
        edge = edge.filter(ImageFilter.CONTOUR)
    if var_smooth.get() == 1:
        edge = edge.filter(ImageFilter.SMOOTH)
    if var_sharpen.get() == 1:
        edge = edge.filter(ImageFilter.SHARPEN)


    edge = np.array(edge)
    if binarize.get() == 1:
        edge = binarize_array(edge, low_threshold=int(low_threshold), threshold=int(g_threshold))

    edge = ImagePIL.fromarray(edge)


    # edge.show()
    image_to_show = ImageTk.PhotoImage(edge)
    panel2 = Label(master, image=image_to_show)
    panel2.image = image_to_show
    panel2.place(x=650, y=450)
    panel2.bind("<Button-1>", mouse_pressed_callback)
    panel2.bind("<ButtonRelease-1>", mouse_released_callback)
    #    edge.save('test.png')
    print(edge.size)


def scale_update(x):
    global g_threshold, x_res, y_res, image_resize_width, image_resize_height
    # print("Threshold = " + str(x))
    # g_threshold = int(x);
    g_threshold = scale1_var.get()
    convert_image()


def scale_update2(x):
    global low_threshold, x_res, y_res, image_resize_width, image_resize_height
    # print("Threshold = " + str(x))
    # low_threshold = scale1
    low_threshold = scale2_var.get()
    convert_image()


def get_pixel_coord(img_array, rows, cols):
    num_pixels = 0
    connected = 0
    for i in range(2, rows - 2):
        for j in range(2, cols - 2):
            if img_array[i][j] == 0:
                connected = 1
                return i, j, connected
    return 0, 0, 0


def get_pixel_connected(img_array, rows, cols, num_cols, num_rows):
    is_connect = 0
    # print(cols)
    # print(rows)

    if rows > 0 and cols > 0 and cols < (num_cols - 1) and rows < (num_rows - 1):
        if img_array[rows - 1][cols] == 0:
            is_connect = 1
            return (rows - 1), cols, is_connect
        if img_array[rows - 1][cols + 1] == 0:
            is_connect = 1
            return (rows - 1), (cols + 1), is_connect

        if img_array[rows][cols + 1] == 0:
            is_connect = 1
            return rows, (cols + 1), is_connect

        if img_array[rows + 1][cols + 1] == 0:
            is_connect = 1
            return (rows + 1), (cols + 1), is_connect

        if img_array[rows + 1][cols] == 0:
            is_connect = 1
            return (rows + 1), cols, is_connect

        if img_array[rows + 1][cols - 1] == 0:
            is_connect = 1
            return (rows + 1), (cols - 1), is_connect

        if img_array[rows][cols - 1] == 0:
            is_connect = 1
            return rows, (cols - 1), is_connect

        if img_array[rows - 1][cols - 1] == 0:
            is_connect = 1
            return (rows - 1), (cols - 1), is_connect

    return 0, 0, 0


def get_num_pixels(img_array, cols, rows):
    num_pixels = 0
    for i in range(2, rows - 2):
        for j in range(2, cols - 2):
            if img_array[i][j] == 0:
                num_pixels = num_pixels + 1
    return num_pixels


def find_paths(img_array, cols, rows):
    global progress1
    pixel_list = []
    path_list = []
    pixels_left = 0
    pixels_left = get_num_pixels(img_array, cols, rows)
    total_pixels = pixels_left
    # print(pixels_left)
    # print("COORD: " +str(row_pos) + " " +str(col_pos))

    while pixels_left > 0:
        # print("STARTING!!!!!")
        # print(pixels_left)

        percentage = 100 * ((total_pixels - pixels_left) / total_pixels)
        progress1['value'] = int(percentage)
        master.update_idletasks()
        row_pos, col_pos, connected = get_pixel_coord(img_array, rows, cols)
        # print("NEW: " + str(row_pos) + " " + str(col_pos))
        if connected == 1:
            pixel_list.append((col_pos, row_pos))
            img_array[row_pos][col_pos] = 255
            pixels_left = pixels_left - 1
        row_pix, col_pix, connected = get_pixel_connected(img_array, row_pos, col_pos, cols, rows)
        while connected == 1:
            # print("CONNECTED: " +str(row_pix) + " " +str(col_pix) + " " +str(pixels_left)+ " " +str(len(path_list)))
            img_array[row_pix][col_pix] = 255
            row_pos = row_pix
            col_pos = col_pix
            pixel_list.append((col_pos, row_pos))
            pixels_left = pixels_left - 1
            row_pix, col_pix, connected = get_pixel_connected(img_array, row_pos, col_pos, cols, rows)
            # print(pixel_list)

        if len(pixel_list) > 0:
            path_list.append(pixel_list.copy())
            pixel_list.clear()

    # print(path_list)
    return path_list


def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def calc_distance(plist1):
    print("Length of original list: " + str(len(plist1)))
    newlist = []
    distance_f = 0
    distance_l = 0
    shortest_index = 0
    shortest_distance = 100000000000000000000
    reverse = 0

    first_list = plist1[0].copy()
    xl, yl = first_list[-1]
    newlist.append(first_list.copy().copy())
    del plist1[0]

    while len(plist1) > 2:
        shortest_distance = 100000000000000000000
        for i in range(1, len(plist1)):
            tmp_list = plist1[i]
            tmp_xf, tmp_yf = tmp_list[0]
            distance_f = distance(xl, yl, tmp_xf, tmp_yf)
            if distance_f <= shortest_distance:
                shortest_distance = distance_f
                shortest_index = i
                reverse = 0
            tmp_xl, tmp_yl = tmp_list[-1]
            distance_l = distance(xl, yl, tmp_xl, tmp_yl)
            if distance_l < shortest_distance:
                shortest_distance = distance_l
                shortest_index = i
                reverse = 1
        # print("Distance to fisrt point: " +str(distance_f) +" Distance to last Point "+str(distance_l))
        # print("INDEX: " +str(shortest_index) + " " + str(reverse) + str(shortest_distance))
        # print("Length of plist: " + str(len(plist1)))
        if reverse == 1:
            plist1[shortest_index].reverse()
        newlist.append(plist1[shortest_index].copy())
        first_list = plist1[shortest_index].copy()
        del plist1[shortest_index]
        xl, yl = first_list[-1]

    # print(plist1[shortest_index])
    # print(newlist)
    # print(len(newlist))
    return newlist


def join(original_list, index):
    shorten = 0
    join_thresh = int(spacing.get())
    # print("Index = " +str(index))
    modified_list = []
    tmp_list = []
    # print("Length of orginal list: " + str(len(original_list)) + " paths")
    len_orig = len(original_list)
    # print(len_orig)
    tmplst1 = original_list[index]
    tmplst2 = original_list[index + 1]
    xf, yf = tmplst1[0]
    xl, yl = tmplst2[0]
    dist = distance(xf, yf, xl, yl)
    # print("Distance  is " +str(dist) +": " +str(xf) + " " +str(yf) + " " +str(xl) + " " +str(yl) + " ")
    #print(join_thresh)
    if dist < join_thresh:
        # print("Can shorten")
        shorten = 1
        tmplst1 = original_list[index]
        for i in range(len(original_list[index])):
            tmp_list.append(tmplst1[i])
            # print(tmplst1[i])
        tmplst1 = original_list[index + 1]
        for i in range(len(original_list[index + 1])):
            tmp_list.append(tmplst1[i])
            # print(tmplst1[i])
        # tmp_list.append(tmplst1)
        # print(tmp_list)
        return shorten, tmp_list
    else:
        shorten = 0
        # print("Appending")
        # modified_list.append(original_list[index])
        # print(original_list[index])
        return shorten, original_list[index]


def join_shortened(optimised_list):
    short = 0
    tmplist = []
    shortened_list = []
    resurse_list = []

    len_orig = len(optimised_list)
    len_new = 0
    # print(len_orig)
    noshorten = 1
    while noshorten == 1:
        noshorten = 0
        while len_new < (len_orig-1):
            short, tmplist = join(optimised_list, len_new)
            #print(tmplist)
            if short == 1:
                noshorten = 1
                del optimised_list[len_new + 1]
                len_orig = len(optimised_list)
                # print("New length = " + str(len_orig))
            shortened_list.append(tmplist)
            len_new = len_new + 1
        noshorten = 0
        #optimised_list = []
        #optimised_list = shortened_list.copy()
        #len_orig = len(optimised_list)
        #if noshorten == 1:
        #    shortened_list = []
        #len_new = 0
    shortened_list.append(optimised_list[-1])  # Add last list as it could not be shortened
    # print("Len New " +str(len_new))
    # print("Len Orig " +str(len_orig))
    return shortened_list


def list_to_gcode(list1):
    len_list = len(list1)
    gcode_list = []

    MyFile = open('output.nc', 'w')

    image_resize_width = int(x_res.get())
    image_resize_height = int(y_res.get())

    print("GCODE: " + str(image_resize_width) + str(image_resize_height))

    for i in range(len_list):
        sublist = list1[i]
        for j in range(len(sublist)):
            x, y = sublist[j]
            x = x * image_resize_width / image_width
            y = y * image_resize_height / image_height
            if j == 0:
                gcode_list.append("G0Z5F800\n")
                gcode_list.append("G1X" + str(x) + "Y" + str(y) + "\n")
                gcode_list.append("G0Z-1F800\n")
                gcode_list.append("F800\n")
            else:
                string1 = "G0X" + str(x) + "Y" + str(y) + "\n"
                gcode_list.append(string1)

    for element in gcode_list:
        MyFile.write(element)
    # print(gcode_list)
    MyFile.close()


def visualise_gcode(final_list):
    # print("Number of paths to draw: " +str(len(final_list)))
    c1.delete("all")
    for i in range(len(final_list)):
        line_coords = final_list[i]
        # print("Number of point to draw in this path: " + str(len(line_coords)))
        for j in range(len(line_coords) - 1):
            x1, y1 = line_coords[j]
            x2, y2 = line_coords[j + 1]
            c1.create_line(x1, y1, x2, y2)


def generate_gcode():
    global edge, labelprogress
    new_path_list = []
    array_img = np.array(edge)
    array_rows, array_cols = array_img.shape
    print("Number of rows: " + str(array_rows) + "Number of cols: " + str(array_cols))
    print("Finding linked paths in image..")
    labelprogress['text'] = "Finding linked paths...."
    master.update_idletasks()
    path_list = find_paths(array_img, array_cols, array_rows)
    print("Deleting short paths...")
    labelprogress['text'] = "Deleting short paths...."
    master.update_idletasks()

#    for i in range(len(path_list)):
#        sub_list = path_list[i]
#        if len(sub_list) > int(remove_short.get()):
#            new_path_list.append(sub_list)
    new_path_list = path_list
    print("Optimising path distance...")
    labelprogress['text'] = "Optomising...."
    master.update_idletasks()
    new_list = calc_distance(new_path_list)

    print("Joining paths with small gaps..")
    labelprogress['text'] = "Joining paths...."
    master.update_idletasks()
    length_before = len(new_list)
    start_length = len(new_list)
    end_length = 0

    while start_length != end_length:
        start_length = len(new_list)
        new_list = join_shortened(new_list)
        end_length = len(new_list)
        print("Partial Optimisatipon of " + str(100 * (length_before-end_length) / length_before) + "%")

    for i in range(len(new_list)):
        sub_list = new_list[i]
        if len(sub_list) > int(remove_short.get()):
            new_path_list.append(sub_list)

    new_list = new_path_list
    #new_list = calc_distance(new_list)
    length_after = len(new_list)
    # print("Final length = " + str(len(new_list)))
    print("Generating GCODE...")
    labelprogress['text'] = "Genertating Gcode...."
    master.update_idletasks()
    list_to_gcode(new_list)
    labelprogress['text'] = "Drawing..."
    master.update_idletasks()
    print("Done!!!")
    print("Optimisatipon of " + str(100 * (length_before - length_after) / length_before) + "%")
    visualise_gcode(new_list)
    labelprogress['text'] = "Done..."
    master.update_idletasks()

def update_image():
    convert_image()


def mouse_released_callback(event):
    global end_x, end_y, convert_section
    print("Mouse button release " + str(event.x) + " " + str(event.y))
    end_x = event.x
    end_y = event.y
    convert_section = 1
    modify_final()


def mouse_pressed_callback(event):
    global start_x, start_y
    print("Mouse button pressed " + str(event.x) + " " + str(event.y))
    start_x = event.x
    start_y = event.y


def main():
    global filename, var1, var2, progress1, labelprogress,panel2
    master.geometry("1280x900")
    master.title("ImageToGCodeGenerator")
    b1 = Button(master, text="Open File", command=callback)
    b1.place(x=20, y=20)
    b2 = Button(master, text="Convert Image", command=convert_image)
    b2.place(x=160, y=20)

    b3 = Button(master, text="Generate Gcode", command=generate_gcode)
    b3.place(x=300, y=20)

    c1.place(x=600, y=30)

    chk1 = Checkbutton(master, text="EdgeDetect", variable=var1, command=update_image)
    chk1.place(x=20, y=60)

    chk2 = Checkbutton(master, text="Invert", variable=var2, command=update_image)
    chk2.place(x=20, y=90)

    chk3 = Checkbutton(master, text="Binarise", variable=binarize, command=update_image)
    chk3.place(x=20, y=125)

    chk4 = Checkbutton(master, text="Blur", variable=var_blur, command=update_image)
    chk4.place(x=150, y=60)

    chk5 = Checkbutton(master, text="Contour", variable=var_contour, command=update_image)
    chk5.place(x=240, y=60)

    chk6 = Checkbutton(master, text="Smooth", variable=var_smooth, command=update_image)
    chk6.place(x=330, y=60)

    chk6 = Checkbutton(master, text="Sharpen", variable=var_sharpen, command=update_image)
    chk6.place(x=150, y=90)


    progress1 = Progressbar(master, length=250, mode='determinate')
    progress1.place(x=20, y=250)

    progress1['value'] = 0

    #    scale1 = Scale(master,from_=0,to=255,orien=HORIZONTAL,command=scale_update,length=250)
    scale1 = Scale(master, from_=0, to=255, orien=HORIZONTAL, length=250, variable=scale1_var)
    scale1.bind("<ButtonRelease-1>", scale_update)
    scale1.place(x=20, y=160)
    label_high_th = Label(master, text="Upper Black Threshold")
    label_high_th.place(x=280, y=180)

    scale2 = Scale(master, from_=0, to=255, orien=HORIZONTAL, length=250, variable=scale2_var)
    scale2.place(x=20, y=200)
    scale2.bind("<ButtonRelease-1>", scale_update2)
    label_low_th = Label(master, text="Lower Black Threshold")
    label_low_th.place(x=280, y=220)

    tBox1 = Entry(master, text="Xres", textvariable=x_res, width=5)
    tBox1.insert(0, '400')
    tBox1.place(x=20, y=300)
    tbox1_label = Label(master, text="Required width of gcode(mm)")
    tbox1_label.place(x=70, y=300)

    tBox2 = Entry(master, text="Yres", textvariable=y_res, width=5)
    tBox2.insert(0, '300')
    tBox2.place(x=20, y=330)
    tbox2_label = Label(master, text="Required height of gcode(mm)")
    tbox2_label.place(x=70, y=330)

    tBox3 = Entry(master, textvariable=spacing, width=5)
    tBox3.insert(0, '2')
    tBox3.place(x=20, y=360)
    tbox3_label = Label(master, text="Join points seperated by(mm)")
    tbox3_label.place(x=70, y=360)

    tBox3 = Entry(master, textvariable=remove_short, width=5)
    tBox3.insert(0, '2')
    tBox3.place(x=20, y=390)
    tbox3_label = Label(master, text="Remove paths shorter than(mm)")
    tbox3_label.place(x=70, y=390)


    print("XRES" + str(tBox1.get()))

    labelprogress = Label(master, text="Current Task: Idle")
    labelprogress.place(x=20, y=270)
    # labelprogress['text'] = "Hello"

    master.mainloop()


main()
