# Read in labels in xml form and convert them into appropriate YOLOv5 dataset format
# Split data into train and test sets (80-20 ratio)

from bs4 import BeautifulSoup
import os
import shutil
from tqdm import tqdm

for idx, path in tqdm(enumerate(os.listdir('data/annotations'))):
    with open(f'data/annotations/Cats_Test{idx}.xml', 'r') as f:
        data = f.read()

    bs_data = BeautifulSoup(data, 'xml')
    xmin = bs_data.find('xmin') 
    ymin = bs_data.find('ymin') 
    xmax = bs_data.find('xmax') 
    ymax = bs_data.find('ymax')
    w = bs_data.find('width')
    h = bs_data.find('height')
    name = bs_data.find('name')

    for tag1, tag2, tag3, tag4, tag5, tag6, tag7 in zip(xmin, ymin, xmax, ymax, w, h, name):
        xmin = float(tag1.string.strip())
        ymin = float(tag2.string.strip())
        xmax = float(tag3.string.strip())
        ymax = float(tag4.string.strip())
        w = float(tag5.string.strip())
        h = float(tag6.string.strip())
        name = tag7.string.strip()

    # print(xmin, ymin, xmax, ymax, w, h)

    x_center = (xmax + xmin) / w / 2.0
    width = (xmax - xmin) / w
    y_center = (ymax + ymin) / h / 2.0
    height = (ymax - ymin) / h

    if name == "cat":
        label = 0
    else:
        label = 1

    wr = f"{label} {x_center} {y_center} {width} {height}"

    if os.path.exists(f"data/labels/Cats_Test{idx}.txt") == False:
        f = open(f"data/labels/Cats_Test{idx}.txt", 'w')
    else:
        with open(f"data/labels/Cats_Test{idx}.txt", 'w') as f:
            f.write(wr)
            f.close()

# Divide into differnt groups "train" "valid"

img = os.listdir('data/images')
label = os.listdir('data/labels')

os.makedirs("data/train/images", exist_ok=True)
os.makedirs("data/train/labels", exist_ok=True)
os.makedirs("data/valid/images", exist_ok=True)
os.makedirs("data/valid/labels", exist_ok=True)

# Train file
for i in tqdm(img[0:2949]):

    j = i.replace("png", "txt")
    source_im = r'data/images'
    target_im = r'data/train/images'

    source_im = source_im + "/" + i
    target_im = target_im + "/" + i

    if not os.path.exists(target_im):
        shutil.copyfile(source_im, target_im)

    source_lb = r'data/labels'
    target_lb = r'data/train/labels'

    source_lb = source_lb + "/" + j
    target_lb = target_lb + "/" + j

    if not os.path.exists(target_lb):
        shutil.copyfile(source_lb, target_lb)

# Valid file
for i in tqdm(img[2949:]):

    j = i.replace("png", "txt")
    source_im = r'data/images'
    target_im = r'data/valid/images'

    source_im = source_im + "/" + i
    target_im = target_im + "/" + i

    if not os.path.exists(target_im):
        shutil.copyfile(source_im, target_im)

    source_lb = r'data/labels'
    target_lb = r'data/valid/labels'

    source_lb = source_lb + "/" + j
    target_lb = target_lb + "/" + j

    if not os.path.exists(target_lb):
        shutil.copyfile(source_lb, target_lb)