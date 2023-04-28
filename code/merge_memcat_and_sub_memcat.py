import csv
import os
from os import walk
from difflib import SequenceMatcher

submemcat = []
with open("data/submemcat-data.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    submemcat.extend(
        [
            row["image"],
            row["category"],
            row["h"],
            row["f"],
            row["n_resp"],
            row["rank"],
        ]
        for row in reader
    )
semmem = []
with open("data/sub_memcat-vs-memcat.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    semmem.extend(
        [
            row["SemMem"],
            row["MemCat"],
        ]
        for row in reader
    )
for i in submemcat:
    check = True
    for s in semmem:
        temp_s = s[0]
        temp_i = i[0]
        if SequenceMatcher(a=temp_s, b=temp_i).ratio() > 0.9:
            print(", ".join(i) + ", " + s[1])
            check = False
            break
    if check == True:
        print(", ".join(i))


semmem = []
with open("data/semmem-vs-memcat.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    semmem.extend(
        [
            row["SemMem"],
            row["category"],
            row["h"],
            row["f"],
            row["n_resp"],
            row["rank"],
            row["MemCat"],
        ]
        for row in reader
    )
memcat = []
with open("memcat_image_data.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    memcat.extend(
        [
            row["image_file"],
            row["H"],
            row["FA"],
            row["n_resp"],
            row["memorability_wo_fa_correction"],
        ]
        for row in reader
    )
for s in semmem:
    check = True
    for m in memcat:
        temp_s = s[6].strip()
        temp_m = m[0].strip()
        if SequenceMatcher(a=temp_s, b=temp_m).ratio() > 0.9:
            print(", ".join(s) + ", " + ", ".join(m))
            check = False
            break
    if check == True:
        print(", ".join(s))
