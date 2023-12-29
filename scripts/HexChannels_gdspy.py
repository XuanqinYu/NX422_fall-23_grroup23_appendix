import numpy as np
import gdspy as gd
import math

#PyScript to automatically generate a hex GDS design
#Created by Nicolas Zaugg as part of Neural Interfaces Group Project, EPFL
#Uses gdspy: https://gdspy.readthedocs.io/en/stable/gettingstarted.html#loading-a-gdsii-file

#Parameters of the unit hex cell
theta = 30
l_b = 350
t = 50
fillet_r = 8

#Parameters of the honeycomb array
device_size = 20000

# The GDSII file is called a library, which contains multiple cells.
lib = gd.GdsLibrary()

#full_gds = lib.new_cell("Full_Gds")
device_array = lib.new_cell("Device_Array")


#caluclate outer length
l = l_b + (t/2) * (1/math.cos(math.radians(theta)))

#trig
c = math.cos(math.radians(60))
s = math.sin(math.radians(60))
offset_x = t/2
#offset_y = t/(4*math.sin(math.radians(30)))
offset_y = (l-l_b)

#Width Unit cell
w = t+2*(math.sin(math.radians(60))*l_b)
#Height Unit cell
h = 2*c*l+l

#inner wdith, height
w_b = 2*(math.sin(math.radians(60))*l_b)
h_b = 2*c*l_b+l_b

#nb of cells
n_rows = math.ceil(0.5*math.ceil(device_size/h))+1
n_columns = math.floor(device_size/w)


#Unit Hex
hex = lib.new_cell('Hex')

#Inner & outer hex geometry parametrization
points_ohex = [(0, l*c), (0, l*c+l), (l*s, 2*l*c+l), (2*l*s, l*c+l), (2*l*s, l*c), (l*s, 0)]
points_ihex = [(0, l_b*c), (0, l_b*c+l_b), (l_b*s, 2*l_b*c+l_b), (2*l_b*s, l_b*c+l_b), (2*l_b*s, l_b*c), (l_b*s, 0)]
hex_2D = gd.boolean(gd.Polygon(points_ohex), gd.Polygon(points_ihex).translate(offset_x, offset_y).fillet(fillet_r), "not")

hex.add(hex_2D)

#Array geometry parametrization
hex_array = lib.new_cell("Hex_Array")

#Offset rows
magic_offset_x = 500
offset_rows = (w/2-magic_offset_x, -(h/2 + l/2))

#Arrays of even and odd rows
arr1 = gd.CellArray(hex, 2*n_columns, 2*n_rows, (w, h+l), (-magic_offset_x,0))
arr2 = gd.CellArray(hex, 2*n_columns, 2*n_rows, (w, h+l), (offset_rows))


#frame

iframe = gd.Rectangle([t, t], [device_size-t, device_size-t])
oframe = gd.Rectangle([0, 0], [device_size, device_size] )

frame = gd.boolean(oframe, iframe, 'not')

#cut
arr1_Cut = gd.boolean(arr1, iframe, 'and')
arr2_Cut = gd.boolean(arr2, iframe, 'and')

hex_array.add(arr1_Cut)
hex_array.add(arr2_Cut)
hex_array.add(frame)

#hex_array.add(arr1)
#hex_array.add(arr2)
#hex_array.add(frame)






lib.write_gds("TEST_Electrode.gds")

#gd.LayoutViewer()