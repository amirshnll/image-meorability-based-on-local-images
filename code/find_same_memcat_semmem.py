from PIL import Image
import shutil
import os
import numpy as np
import csv
import os
from os import walk
from defs.utils import make_new_folder

current_folder = "image/memcat"

list_dir = ["animal", "food", "landscape", "sports", "vehicle"]
# list_dir = ['airplane', 'champagne', 'geyser', 'mouse', 'soup', 'american-football', 'cheese', 'giraffe', 'muffin', 'squirrel', 'apple', 'chicken', 'golf', 'orange', 'subway-train', 'archery', 'climbing', 'gravy', 'pasta', 'surfing', 'badlands', 'cocktail', 'gymnastics', 'pasture', 'suv', 'bagel', 'coffee', 'hamster', 'pigeon', 'swimming', 'banana', 'cow', 'helicopter', 'pizza', 'tea', 'barbecue', 'creek', 'horse', 'plantation', 'tennis', 'barn', 'cricket', 'hot-air-balloon', 'pleasure-boat', 'tow-truck', 'baseball', 'deer', 'hotdog', 'rabbit', 'track-and-field', 'basketball', 'desert', 'ice-hockey', 'river', 'tractor', 'bear', 'dog', 'icescape', 'roller-skating', 'train', 'bell-pepper', 'donut', 'japanese-martial-arts', 'rowing', 'tram', 'bicycle', 'duck', 'juice', 'rugby', 'truck', 'bicycling-racing', 'elephant', 'jungle', 'salad', 'tundra', 'boxing', 'fencing', 'karate', 'sandwich', 'valley', 'bread', 'field', 'lacrosse', 'savanna', 'volcano', 'breakfast', 'field-hockey', 'lake', 'scooter', 'volleyball', 'broccoli', 'figure-skating', 'limousine', 'sea', 'waterfall', 'burrito', 'fishing-boat', 'lion', 'sheep', 'wetland', 'bus', 'fitness', 'mangrove', 'shore', 'wild-boar', 'butternut-squash', 'forest-broadleaf', 'marten', 'skateboarding', 'windmill', 'cable-car', 'forest-needleleaf', 'mashed-potato', 'skiing', 'yacht', 'cake', 'forklift', 'moor', 'snowboarding', 'yogurt', 'camper', 'fox', 'motorcycle', 'snowmobile', 'zebra', 'car', 'freighter', 'mountain', 'snowscape', 'zucchini', 'cat', 'frisbee', 'mountain-biking', 'soccer']

content_list = {}
for index, val in enumerate(list_dir):
    path = os.path.join(current_folder, val)
    content_list[list_dir[index]] = os.listdir(path)

merge_folder = "merge_folder"
merge_folder_path = os.path.join(current_folder, merge_folder)
make_new_folder(merge_folder, current_folder)

for sub_dir in content_list:
    for contents in content_list[sub_dir]:
        path_to_content = sub_dir + "/" + contents
        dir_to_move = os.path.join(current_folder, path_to_content)
        shutil.move(dir_to_move, merge_folder_path)

sub_memcat = []

with open("data/sub_memcat-data.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        try:
            if row["category"] == "iran":
                continue
            else:
                file_image = row["\ufeffimage"]
                img1 = Image.open("image/sub_memcat/" + file_image)

                sub_memcat.append(
                    {"filename": file_image, "data": np.array(img1.convert("L"))}
                )
                img1.close()
        except:
            continue

memcat = []
img = ""
i = 1
for file in os.listdir("image/memcat/"):
    # remove mac .DS_Store file
    if file == ".DS_Store":
        continue
    img = Image.open("image/memcat/" + file)
    memcat.append({"filename": file, "data": np.array(img.convert("L"))})
    img.close()
    i += 1

for img1 in sub_memcat:
    for img2 in memcat:
        if np.array_equal(img1["data"], img2["data"], equal_nan=True):
            print(img1["filename"] + " - " + img2["filename"])
