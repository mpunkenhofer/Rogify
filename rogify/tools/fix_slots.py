import __about__
import argparse

from rogify.base.util import (file_exists, load_items, store_items)
from rogify.__config__ import slot_synonyms


def resolve_unknown_slots(items):
    fixed_items = []

    choice_dict = {i: k for i, k in enumerate(slot_synonyms.keys())}

    for item in items:
        if item.slot not in slot_synonyms.keys():
            print('\n{}\n-> Unknown Slot Type!'.format(item))

            choice = -1

            while choice not in choice_dict.keys():
                print(choice_dict)
                choice = int(input('Slot: '))

            item.slot = choice_dict[choice]

            fixed_items.append(item)
        else:
            fixed_items.append(item)

    return fixed_items


def main():
    parser = argparse.ArgumentParser(
        description='DAoC Rogify DB Slot Fix! v{}.\nClassify Unknown Slot Items!'.format(
            __about__.__version__))

    parser.add_argument('database', type=str,
                        help='Rogify DB file')
    parser.add_argument('-o', '--output', type=str, default='items.json',
                        help='output file name')

    args = parser.parse_args()

    if not file_exists(args.database):
        print("Error: file '%s' does not exists." % args.database)
        return 1

    if file_exists(args.output):
        print("Error: output file '%s' already exists." % args.output)
        return 1

    items = load_items(args.database)
    fixed_items = resolve_unknown_slots(items)
    store_items(args.output, fixed_items)

    print("Done!")


if __name__ == "__main__":
    main()
