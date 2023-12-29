import numpy as np
import gdspy as gd
import math

#PyScript to automatically generate a hex-microhole array GDS design
#Created by Nicolas Zaugg as part of Neural Interfaces Group Project, EPFL
#Uses gdspy: https://gdspy.readthedocs.io/en/stable/gettingstarted.html#loading-a-gdsii-file



# The GDSII file is called a library, which contains multiple cells.
lib = gd.GdsLibrary()
chip = lib.new_cell("Chip")

#------------------------------------------------------
#parameters of the parameter_square
p_square = (1400, 1400)
label_size = 25
pos_array = (600, 800)


#parameters of the array
r = 5 
d_array = 20000

device_size = 20000
psa_s = 600
#Parameters of the unit honecomb cell (see word doc)
theta = 30

t = 10
fillet_r = 8

#------------------------------------------------------





l_b = 2**2*r

#if (i>2): 
    #offset_x = offset_x - 3*psa_s

#caluclate outer length
#l = l_b + (t/2) * (1/math.cos(math.radians(theta)))

#trig
c = math.cos(math.radians(60))
s = math.sin(math.radians(60))
#offset_x = t/2
#offset_y = t/(4*math.sin(math.radians(30)))
#offset_y = (l-l_b)

#Width Unit cell
w = (math.sin(math.radians(60))*l_b)
#Height Unit cell
h =c*l_b+l_b

#nb of cells
n_rows = 2*math.ceil(0.5*math.ceil(device_size/h))+1
n_columns = math.floor(device_size/w)

points_ihex = [(0, l_b*c), (0, l_b*c+l_b), (l_b*s, 2*l_b*c+l_b), (2*l_b*s, l_b*c+l_b), (2*l_b*s, l_b*c), (l_b*s, 0)]



# Create single hole
single_Hole = lib.new_cell('Hole_')
single_Hole.add(gd.Round((0, 0), r))


hex_Holes = lib.new_cell('hex_Holes_')
hex_Holes.add(gd.CellReference(single_Hole, points_ihex[0]))
hex_Holes.add(gd.CellReference(single_Hole, points_ihex[1]))
hex_Holes.add(gd.CellReference(single_Hole, points_ihex[2]))
hex_Holes.add(gd.CellReference(single_Hole, points_ihex[3]))
hex_Holes.add(gd.CellReference(single_Hole, points_ihex[4]))
hex_Holes.add(gd.CellReference(single_Hole, points_ihex[5]))


#Offset rows
offset_rows = (w/2, -(h/2 + l_b/2))

p_array = (4*r, 4*r)
#Full Square
square = gd.Cell("Square_")


square.add(gd.CellArray(single_Hole, n_columns, n_rows, (w, h), (600, 800)))
square.add(gd.CellArray(single_Hole, n_columns, n_rows, (w, h), (w/2+600, 800-(h/2))))

#Add to Full Chip
chip.add(square)
#chip.add(single_Hole)
##chip.add(square_label)



#chip.add(gd.CellArray(single_Hole, n, n, p_array, (600+offset_x, 800+offset_y)))
# Save the library in a file called 'first.gds'.
lib.write_gds('M4_TestH.gds')

# Optionally, save an image of the cell as SVG.
#single_Hole.write_svg('first.svg')

# Display all cells using the internal viewer.
#gd.LayoutViewer()