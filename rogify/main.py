# Author: Punkenhofer Mathias
# Mail: code.mpunkenhofer@gmail.com
# Date: 09.02.2019

import __about__
import argparse
import itertools
import json

from rogify.base.util import (file_exists, load_items, encode_item)
from rogify.__config__ import (slot_synonyms, attributes, attribute_synonyms)


class Rogify:
    def __init__(self, database):
        items = load_items(database)
        self.slots = self.group_items(items)

        self.slot_list = [l for l in self.slots.values()]

        # Duplicate Rings & Bracers (2 Slots of each)
        if 'Ring' in self.slots and len(self.slots['Ring']) > 1:
            self.slot_list.append(self.slots['Ring'])
        if 'Wrist' in self.slots and len(self.slots['Wrist']) > 1:
            self.slot_list.append(self.slots['Wrist'])

        self.attribute_synonyms = {k.lower(): v for k, v in attribute_synonyms.items()}

        self.combinations = []

        self.best_eval = (float("-inf"), {})

    def rogify(self, intermediate):
        # self.combinations = list()

        for c in itertools.product(*self.slot_list):
            # check for duplicates
            if any(c.count(x) > 1 for x in c):
                continue

            ev = self.eval(c)
            best_ev, _ = self.best_eval

            if ev > best_ev:
                self.best_eval = ev, c

                if intermediate:
                    self.short_report()

    def report(self):
        ev, items = self.best_eval

        attribute_total = self.attribute_sum(items)
        attribute_report = {}

        for k, v in attribute_total.items():
            cap, fun = attributes[k]

            x = max(0, min(cap, attribute_total[k]))

            attribute_report[k] = '{} ({:+})'.format(x, v - cap)

        grouped_items = {k: [encode_item(i) for i in v] for k, v in self.group_items(items).items()}

        r = json.dumps((attribute_report, grouped_items), indent=2)

        print('\nBest EV: {}\n{}\n'.format(ev, r))

        return r

    def short_report(self):
        ev, items = self.best_eval

        attribute_total = self.attribute_sum(items)
        attribute_report = {}

        for k, v in attribute_total.items():
            cap, fun = attributes[k]

            x = max(0, min(cap, attribute_total[k]))

            attribute_report[k] = '{} ({:+})'.format(x, v - cap)

        item_names = [i.name for i in items]

        r = json.dumps((attribute_report, item_names), indent=2)

        print('\nBest EV: {}\n{}\n'.format(ev, r))

        return r

    def eval(self, items):
        attribute_total = self.attribute_sum(items)
        ev = 0

        for k, v in attributes.items():
            attribute_type = k
            cap, fun = v

            if attribute_type in attribute_total:
                x = max(0, min(cap, attribute_total[attribute_type]))
                ev += fun(x)

        return ev

    def attribute_sum(self, items):
        attribute_total = {}

        for i in items:
            for a in i.attributes:
                if a.type.lower() in self.attribute_synonyms.keys():
                    for sa in self.attribute_synonyms[a.type.lower()]:
                        if sa in attribute_total:
                            attribute_total[sa] += a.value
                        elif sa in attributes.keys():
                            attribute_total[sa] = a.value
                else:
                    if a.type in attribute_total:
                        attribute_total[a.type] += a.value
                    elif a.type in attributes.keys():
                        attribute_total[a.type] = a.value

        return attribute_total

    @staticmethod
    def group_items(items):
        slots = {}

        for i in items:
            if i.slot in slots:
                slots[i.slot].append(i)
            elif i.slot in slot_synonyms.keys():
                slots[i.slot] = [i]

        return slots


def main():
    print('Rogify! v{}'.format(__about__.__version__))

    parser = argparse.ArgumentParser(
        description='Rogify! v{}.\nOutputs the best possible combination of rogs for your character!'.format(
            __about__.__version__))

    parser.add_argument('database', type=str,
                        help='Rogify DB file')
    parser.add_argument('-o', '--output', type=str, default='report.json',
                        help='report file name')
    parser.add_argument('-i', '--intermediate', action='store_true',
                        help='display intermediate best calculations')

    args = parser.parse_args()

    if not file_exists(args.database):
        print("Error: file '%s' does not exists." % args.database)
        return 1

    if file_exists(args.output):
        print("Error: output file '%s' already exists." % args.output)
        return 1

    print('Loading and categorizing DB ...')

    r = Rogify(args.database)

    print('Contemplating rogs ...')

    r.rogify(args.intermediate)

    report = r.report()

    with open(args.output, 'w') as f:
        f.write(report)

    print('Done!')


if __name__ == "__main__":
    main()
