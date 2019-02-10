# Author: Punkenhofer Mathias
# Mail: code.mpunkenhofer@gmail.com
# Date: 09.02.2019

import __about__
import argparse
import re

from rogify.base.item import (Attribute, Item, Slot)
from rogify.base.util import (file_exists, store_items)


def parse_log(filename):
    items = []

    reg_begin = re.compile(r"[^<]+<Begin Info:([^>]+)>")
    reg_end = re.compile(r"[^<]+<End Info>")
    reg_resist = re.compile(r"[^\|]+\|\s([^:]+):\s*\+(\d+)\s*\%")
    reg_stat = re.compile(r"[^\|]+\|\s([^:]+):\s*\+(\d+)\s*pts")

    with open(filename) as f:
        try:
            line = next(f)

            while line:
                m = reg_begin.match(line)

                if m:
                    item_name = m.group(1).strip()
                    attributes = []

                    line = next(f)

                    while line and not reg_end.match(line):
                        m = reg_resist.match(line)

                        if m:
                            attributes.append(
                                Attribute('{} Resist'.format(m.group(1).strip()), int(m.group(2).strip())))
                        else:
                            m = reg_stat.match(line)

                            if m:
                                attributes.append(Attribute('{}'.format(m.group(1).strip()), int(m.group(2).strip())))

                        line = next(f)

                    items.append(Item(item_name, Slot(item_name), attributes))

                line = next(f)
        except StopIteration:
            return items

    return items


def main():
    parser = argparse.ArgumentParser(
        description='DAoC ChatLog to Rogify DB! v{}.\nConverts a daoc .log file to Rogify DB format.'.format(
            __about__.__version__))

    parser.add_argument('chatlog', type=str,
                        help='daoc chatlog file')
    parser.add_argument('-o', '--output', type=str, default='items.json',
                        help='output file name')

    args = parser.parse_args()

    print("Parsing chatlog '%s' ..." % args.chatlog)

    if not file_exists(args.chatlog):
        print("Error: chatlog file '%s' does not exists." % args.chatlog)
        return 1

    if file_exists(args.output):
        print("Error: output file '%s' already exists." % args.output)
        return 1

    print("Creating database '%s' ..." % args.output)
    items = parse_log(args.chatlog)

    store_items(args.output, items)

    print("Done!")


if __name__ == "__main__":
    main()
