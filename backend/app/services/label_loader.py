import os
from dotenv import load_dotenv

load_dotenv()

def create_category_index(label_path):
    """
    Creates a category index (used in object detection) from a label file.
    Skips invalid labels like '???' and assigns numeric IDs.
    """
    with open(label_path, "r") as f:
        category_index = {}
        for i, val in enumerate(f):
            if i != 0:
                val = val[:-1]
                if val != '???':
                    category_index.update({(i-1): {'id': (i-1), 'name': val}})
    return category_index

LABEL_PATH = os.getenv("LABEL_PATH")
CATEGORY_INDEX = create_category_index(LABEL_PATH)