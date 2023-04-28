# imports
import os
import uuid


def change():
    path = "./image/memcat"
    category = os.listdir(path)

    # change file name
    i = 101
    for cat in category:
        for file in os.listdir(f"{path}/{str(cat)}/"):
            # remove mac .DS_Store file
            if file == ".DS_Store":
                continue

            new_file_name = f"{uuid.uuid4().hex}.jpg"
            relative_path = f"{path}/{str(cat)}/"
            os.rename(relative_path + file, relative_path + new_file_name)

            i = i + 1
