#!/bin/bash
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

ANNOTATIONS_CSV="$1"
DATASET_FOLDER="$2"
OUTPUT_FOLDER="$3"


for i in `cat ${ANNOTATIONS_CSV}  | cut -d"," -f1`; 
do 
	if [ -e ${DATASET_FOLDER}/$i.jpg ]; then 
		ln -fs ${DATASET_FOLDER}/$i.jpg ${OUTPUT_FOLDER}/$i.jpg; 
	else
		echo "Not found $i.jpg";
	fi;
done
