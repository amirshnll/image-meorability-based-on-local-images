# imports
import csv
from defs.utils import file_exists

# base-path file
data_path = "./data/"

# dataset filename
semmem_file = f"{data_path}semmem-vs-memcat.csv"
memcat_file = f"{data_path}memcat.csv"
lamem_file = f"{data_path}lamem.csv"
figrim_file = f"{data_path}figrim.csv"


def read_dataset(dataset_name):
    if dataset_name == "semmem":
        return read_semmem()
    elif dataset_name == "memcat":
        return read_memcat()
    elif dataset_name == "lamem":
        return read_lamem()
    elif dataset_name == "figrim":
        return read_figrim()
    else:
        return "dataset not found"


def read_semmem():
    semmem = []
    sub_memcat = []

    if file_exists(not semmem_file):
        return semmem, sub_memcat

    with open(semmem_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            semmem.append(float(row["rank_semmem"]))

            if row["rank_memcat"] == "":
                continue
            sub_memcat.append(float(row["rank_memcat"]))
    return semmem, sub_memcat


def read_lamem():
    lamem = []

    if file_exists(not lamem_file):
        return lamem

    with open(lamem_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        lamem.extend(float(row["rank"]) for row in reader)
    return lamem


def read_memcat():
    memcat = []

    if file_exists(not memcat_file):
        return memcat

    with open(memcat_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        memcat.extend(float(row["rank"]) for row in reader)
    return memcat


def read_figrim():
    figrim = []

    if file_exists(not figrim_file):
        return figrim

    with open(figrim_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        figrim.extend(float(row["rank"]) for row in reader)
    return figrim
