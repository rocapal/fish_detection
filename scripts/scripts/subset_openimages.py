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

import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

import sys

# Classes: class-descriptions-boxable.csv
# Training dataset: train-annotations-bbox.csv
# Eval dataset: validation-annotations-bbox.csv

if (len(sys.argv) != 4):
    print ("Usage: python argv[0] classes.csv annotations.csv output.csv")
    exit(-1)

classes_file = sys.argv[1]
annotations_file = sys.argv[2]
output_file = sys.argv[3]

# Read class dict
class_dict = {}
with open(classes_file) as f:
    for line in f:
        cls_id = line.split(',')[0]
        cls = line.split(',')[1][:-1]
        class_dict[cls_id] = cls
        

fish_class_ids = []
for class_id in class_dict:
        if class_dict[class_id] in ['Fish', 'Goldfish']:
                    fish_class_ids += [class_id]
print(fish_class_ids)
print([class_dict[class_id] for class_id in fish_class_ids])

df = pd.read_csv(annotations_file)
df.tail()

df = df.loc[df['LabelName'].isin(fish_class_ids)]
df = df.reset_index(drop=True)
df = df[df['IsGroupOf']==0] # Remove big group of fish

df[['ImageID', 'XMin', 'XMax', 'YMin', 'YMax']].to_csv(output_file, index=False)
                    
