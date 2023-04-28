import csv
import os
from os import walk

i = 1

with open("data/sub_memcat-data.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        extention_file = row["image"].split(".")
        extention_file = extention_file[1]
        new_file = f"000{str(i)}.{extention_file}"
        old_name = "image/sub_memcat/" + row["category"] + "/" + row["image"]
        new_name = "image/sub_memcat/" + row["category"] + "/" + new_file
        os.rename(old_name, new_name)
        i = i + 1

        print(
            f"{new_file}, "
            + row["category"]
            + ", "
            + row["h"]
            + ", "
            + row["f"]
            + ", "
            + row["n_resp"]
            + ", "
            + row["rank"]
        )

num = 0
files = []
for file in walk("image/sub_memcat/fillers/"):
    files.extend(file)

i = 1

for file in os.listdir("image/sub_memcat/fillers/"):
    extention_file = str(file).split(".")
    extention_file = extention_file[1]
    new_file = f"000000{str(i)}.{extention_file}"
    old_name = f"image/sub_memcat/fillers/{str(file)}"
    new_name = f"image/sub_memcat/fillers/{new_file}"
    os.rename(old_name, new_name)
    i = i + 1
