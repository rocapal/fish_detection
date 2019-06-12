#!/usr/bin/python
#
# Copyright (C) 2019 by Roberto Calvo-Palomino
#
#
#  This programa is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Electrosense is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with RTL-Spec.  If not, see <http://www.gnu.org/licenses/>.
# 
# 	Authors: Roberto Calvo-Palomino <rocapal [at] gmail [dot] com>
#
import re
import os
from PIL import Image
import sys

#PATH_TRAINING = "./data/fish_train.csv"
#PATH_IMAGES = "./fish/"

if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print ("Usage: %s dataset.csv output_folder" % (sys.argv[0]))
        exit(-1)

    dataset_file = sys.argv[1]
    output_folder = sys.argv[2]
    
    with open(dataset_file) as f:
        lines = f.readlines()

    for l in lines:
        
        data = l.split(",")        
        try:
            im = Image.open(output_folder + data[0] + ".jpg")
            image_w, image_h = im.size
            
            x_values = [float(data[1]), float(data[2])]
            y_values = [float(data[3]), float(data[4])]
            
            center_x = (x_values[1]+x_values[0])/2
            center_y = (y_values[1]+y_values[0])/2

            w = (x_values[1]-x_values[0])
            h = (y_values[1]-y_values[0])

            print (output_folder + data[0] + ".txt")
            f = open(output_folder + data[0] + ".txt", "a")
            f.write("{} {} {} {} {}\n".format("0", center_x, center_y, w, h))
            f.close()

            
        except IOError:            
            pass

    
