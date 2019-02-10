# Author: Punkenhofer Mathias
# Mail: code.mpunkenhofer@gmail.com
# Date: 09.02.2019

import __about__
import argparse

from rogify.base.util import (file_exists, load_items, store_items)


def merge_dbs(first, second, error_flag):
    items = load_items(first)
    items_second = load_items(second)

    for new_item in items_second:
        if new_item not in items:
            items.append(new_item)
        elif error_flag:
            print('{} already in db!'.format(new_item.name))

    if error_flag:
        print()

    return items


def main():
    parser = argparse.ArgumentParser(
        description='DAoC Rogify DB Merger! v{}.\nMerges two Rogify DB format files.'.format(
            __about__.__version__))

    parser.add_argument('first', type=str,
                        help='Rogify DB first file')
    parser.add_argument('second', type=str,
                        help='Rogify DB second file')
    parser.add_argument('-o', '--output', type=str, default='items.json',
                        help='output file name')
    parser.add_argument('-e', '--errors', action='store_true',
                        help='display merge errors (duplicate items)')

    args = parser.parse_args()

    if not file_exists(args.first):
        print("Error: file '%s' does not exists." % args.first)
        return 1

    if not file_exists(args.second):
        print("Error: file '%s' does not exists." % args.second)
        return 1

    if file_exists(args.output):
        print("Error: output file '%s' already exists." % args.output)
        return 1

    print("Merging files {} and {} into {} ...\n".format(args.first, args.second, args.output))

    items = merge_dbs(args.first, args.second, args.errors)

    store_items(args.output, items)

    print("Done! {} now contains {} items.".format(args.output, len(items)))


if __name__ == "__main__":
    main()
