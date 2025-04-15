def load_labels(label_path):
    with open(label_path, "r") as f:
        return [line.strip() if line.strip() != "???" else "unknown" for line in f.readlines()]

# The function `load_labels` reads a label file and returns a list of labels.
def create_category_index(label_path):
    with open(label_path, "r") as f:
        category_index = {}
        for i, val in enumerate(f):
            if i != 0:
                val = val[:-1]
                if val != '???':
                    category_index.update({(i-1): {'id': (i-1), 'name': val}})
    return category_index

label_path = "models/labelmap.txt"
CATEGORY_INDEX = create_category_index(label_path)