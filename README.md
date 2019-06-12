## Introduction

## YOLO - darknet

Clone the repository:
```bash
$ cd /opt/
$ git clone https://github.com/AlexeyAB/darknet
$ cd /opt/darknet
$ make
```

Note: Edit the Makefile to enable GPU and Cuda support.

## Download datasets

We are going to use the datasets provided by [openimages](https://storage.googleapis.com/openimages/web/index.html) when they already contain annotations of the interesting objects. They offer 600 object classes in 1,743,042 training images, with a full validation (41,620 images) and test (125,436 images) sets.


1. Install awscli (universal Command Line Environment for AWS)
```bash
$ sudo apt install awscli
```

2. Download images for train, validation and test:
```bash
$ aws s3 --no-sign-request sync s3://open-images-dataset/train [target_dir/train] (513GB)
$ aws s3 --no-sign-request sync s3://open-images-dataset/validation [target_dir/validation] (12GB)
$ aws s3 --no-sign-request sync s3://open-images-dataset/test [target_dir/test] (36GB)
```

3. Download the CSV files with all the annotations and classes
```bash
$ wget https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv
$ wget https://storage.googleapis.com/openimages/2018_04/validation/validation-annotations-bbox.csv
$ wget https://storage.googleapis.com/openimages/2018_04/test/test-annotations-bbox.csv
$ wget https://storage.googleapis.com/openimages/2018_04/class-descriptions-boxable.csv
```

Links:
- [1] https://storage.googleapis.com/openimages/web/download.html
- [2] https://github.com/cvdfoundation/open-images-dataset#download-images-with-bounding-boxes-annotations

## Prepare datasets

For now on, let's suppose the following paths: 
 - The directory where images have been downloaded:  /opt/openimages/[train,validation,test]
 - The directory where darknet has been cloned: /opt/darknet/

### Creating the dataset of classes of interest

Since we have download the complete dataset, the first thing is to generate a subset with the classes of interest (e.g. 'fish') that will use for the training.

```bash
$ python subset_openimages.py class-descriptions-boxable.csv fish_train_descriptions.csv
```
Then, 'myclass-descriptions.csv' will contain all the image IDs and annotations for all the classes of interest. Let's have a look at the file

```bash
$ cat fish_train.csv
ImageID,XMin,XMax,YMin,YMax
0000dd8e0cb25756,0.322266,0.895508,0.276565,0.759825
0004e0650dd10f47,0.020365,0.044242000000000004,0.729526,0.759698
 ```
The annotations provided by openimages specify the imageID and the X[max,min] and [Ymax,min] of each rectangle(boxing). We will see in a moment how to convert this notation to the one that YOLO(darknet) understands.

### Conversion of the annotations

To avoid working on the directory where we have downloaded all the images of the dataset, we are going to create another folder for our classes and we will make symbolic links to the original ones. In order to do that execute the following:

```bash
$ mkdir -p /opt/dataset/fish/
$ ./create_subset.sh fish_train_descriptions.csv /opt/openimages/train/ /opt/dataset/fish/
```
YOLO (darknet) expects the following format for every annotation: <object-class> <x_center> <y_center> <width> <height> , which is not the same that the one provided by openimages.

```bash
$ python convert_annotations.py fish_train_descriptions.csv /opt/dataset/fish/
```
After running the previous script you should see something similar in your folder /opt/dataset/fish (one txt file for very jpg file)

```bash
238a0bdf53527e7f.jpg  5b51a5607ad6551d.jpg  91af05f8b8c6914b.jpg  c604101624fffbf2.jpg 
238a0bdf53527e7f.txt  5b51a5607ad6551d.txt  91af05f8b8c6914b.txt  c604101624fffbf2.txt 
```

And you can check that the annotations were converted properly by using the following script. The script will show the image and will plot a rectangle for every annotation found in the txt file:

```bash
$ python check_annotation.py /opt/dataset/fish/238a0bdf53527e7f.jpg
```

![image](/images/fish3.png)

All right! dataset seems to be ready to star the training.

## Training with YOLO - darknet

After compile darknet, go to the working directory ${DARKNET_FOLDER}/darknet/build/darknet/x64  and build the following directory:
```bash
$ mkdir data-fish; cd data-fish/
$ ls /opt/dataset/fish/*jpg > fish_train.txt
$ echo "fish" > obj.names
$ echo "classes= 1
train  = data-fish/train.txt
valid  = data-fish/train.txt 
names = data-fish/obj.names
backup = backup/" > obj.data
```

And copy the file "yolov3-obj.cfg" that you find in this repository to ${DARKNET_FOLDER}/darknet/build/darknet/x64, then you should have the following structure:

```bash
$ ${DARKNET_FOLDER}/darknet/build/darknet/x64
yolov3-obj.cfg 
data-fish/
├── obj.data
├── obj.names
└── train.txt
```
Download the pre-trained  weights (154 MB)
```bash
$  wget http://pjreddie.com/media/files/darknet53.conv.74
```
Start the training:
```bash
$  ./darknet detector train data-fish/obj.data yolov3-obj.cfg darknet53.conv.74
```

More information about the use of darknet, details, tricks .... -> [https://github.com/AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)

## Fish Detection with YOLO - darknet

Download the pre-trained weights (235 MB) for the network trained with 'fish' annotations of openimages dataset
```bash
$  wget https://www.dropbox.com/s/gmw2774nrsw7ovk/yolov3-obj_30000.weights?dl=0
```
Run the detection object
```bash
./darknet detector test data-fish/obj.data yolov3-obj.cfg  yolov3-obj_30000.weights -thresh 0.5 -i 0 test/img_00012.jpg
```

![image](/images/fish1.png)

![image](/images/fish2.png)





Check real time fish detection in this ![video](https://www.dropbox.com/s/6ukrcdwe328aon2/res.avi?dl=0)

## Links

### Datasets
 * https://wiki.qut.edu.au/display/cyphy/Fish+Dataset
 * http://groups.inf.ed.ac.uk/f4k/GROUNDTRUTH/RECOG/
 * http://www.image-net.org/
 * https://swfscdata.nmfs.noaa.gov/labeled-fishes-in-the-wild/

### Papers
 * Yolo_v1: https://arxiv.org/abs/1506.02640
 * Yolo_v2: https://arxiv.org/abs/1612.08242
 * Yolo_v3: https://pjreddie.com/media/files/papers/YOLOv3.pdf
 * Vision based Real-time Fish Detection Using Convolutional Neural Network: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8084889
 * Supporting Ground-Truth annotation of image datasets using clustering: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6460437
 * Labeled fishes in the wild: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7046815

### Misc
 * https://spark-in.me/post/fish-object-detection-ssd-yolo
 * https://www.youtube.com/watch?time_continue=3&v=AFV-FiKUFyI
 * https://storage.googleapis.com/openimages/web/index.html
 * https://medium.com/@monocasero/detecci%C3%B3n-de-objetos-con-yolo-implementaciones-y-como-usarlas-c73ca2489246
 * https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
 * https://github.com/kwea123/fish_detection
 * https://github.com/rafaelpadilla/Object-Detection-Metrics

