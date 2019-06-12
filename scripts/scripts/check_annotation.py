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

import sys
import cv2
import os.path

if (len(sys.argv) !=2):
    print("Usage %s: path_to_image" % sys.argv[0])

image_filename = sys.argv[1]
annotations_filename = image_filename[:-3]+"txt"

if not os.path.exists(image_filename):
    print ("Error: Image file %s does not exist!" % image_filename)
    exit(-1)

if not os.path.exists(annotations_filename):
    print ("Error: annotation file %s does not exist!" % annotations_filename)
    exit(-1)

img = cv2.imread(image_filename)
img_width = img.shape[1]
img_height = img.shape[0]

with open(annotations_filename) as f:
    lines = f.readlines()

for l in lines:
    data = l.split(" ")
    print data
    cx1 = float(data[1])
    cy1 = float(data[2])
    w = float(data[3])
    h = float(data[4])
    x1 = int((cx1 - w/2)*img_width)
    y1 = int((cy1 - h/2)*img_height)
    x2 = int((cx1 + w/2)*img_width)
    y2 = int((cy1 + h/2)*img_height)
    print(x1,y1,x2,y2)
    cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0),2)
    
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

