# imports
import os
import shutil
import random


def get_random_images():
    # paths
    dataset_path = "./image/memcat"
    output_path = "./image/sub_memcat"  # new dataset path

    # get all category
    category = os.listdir(dataset_path)
    if "fillers" in category:
        # we remove fillers because we need target image
        category.remove("fillers")

    subcategory = [os.listdir(f"{dataset_path}/{cat}") for cat in category]
    # image sepration count
    output_count = 830
    output_count_per_category = output_count // len(category)

    for i, sub_cat in enumerate(subcategory):
        sub_cat_count = len(sub_cat)
        image_per_sub_cat = int(output_count_per_category / sub_cat_count)
        for sub in sub_cat:
            list_file_sub = os.listdir(f"{dataset_path}/{str(category[i])}/{sub}")
            for _ in range(image_per_sub_cat):
                file = random.choice(list_file_sub)
                shutil.copy2(
                    f"{dataset_path}/{str(category[i])}/{str(sub)}/{str(file)}",
                    f"{output_path}/{str(category[i])}",
                )
