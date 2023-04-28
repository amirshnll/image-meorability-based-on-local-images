import json
import os.path


def readGeneralizationJson(lang="en"):
    if os.path.exists(lang + ".json"):
        file = open(lang + ".json")
        data = json.load(file)
        file.close()
    return data
