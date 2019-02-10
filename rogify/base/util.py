import json

from pathlib import Path
from rogify.base.item import (decode_item, encode_item)


def file_exists(file_name):
    if Path(file_name).is_file():
        return True
    else:
        return False


def load_items(file):
    with open(file) as f:
        json_items = json.loads(f.read())
        items = [decode_item(i) for i in json_items]

        return items


def store_items(file, items):
    db = json.dumps([encode_item(i) for i in items], indent=2)

    with open(file, 'w') as f:
        f.write(db)
