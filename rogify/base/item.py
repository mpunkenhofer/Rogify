# Author: Punkenhofer Mathias
# Mail: code.mpunkenhofer@gmail.com
# Date: 09.02.2019

from rogify import __config__


class Attribute:
    def __init__(self, type, value):
        self.__type = type
        self.__value = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, t):
        self.__type = t

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.__value = v

    def __str__(self):
        return "{}: {}".format(self.__type, self.__value)

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value


class Slot:
    def __init__(self, slot):
        self.__types = __config__.slot_synonyms
        self.slot = slot

    @property
    def slot(self):
        return str(self.__slot)

    @slot.setter
    def slot(self, t):
        self.__slot = "Unknown"

        for slot, synonyms in self.__types.items():
            for synonym in synonyms:
                if t.lower().find(synonym.lower()) > 0:
                    self.__slot = slot
                    return

    def __str__(self):
        return self.slot

    def __eq__(self, other):
        return self.slot.lower() == other.slot.lower()


class Item:
    def __init__(self, name, slot, attributes):
        self.name = name
        self.slot = slot
        self.attributes = attributes

    @property
    def attributes(self):
        return self.__attributes

    @attributes.setter
    def attributes(self, a):
        self.__attributes = a

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, n):
        self.__name = n

    @property
    def slot(self):
        return str(self.__slot)

    @slot.setter
    def slot(self, s):
        self.__slot = s

    def __str__(self):
        return '{} ({})\n{}'.format(self.name, self.slot, '\n'.join([str(s) for s in self.attributes]))

    def __eq__(self, other):
        return self.slot == other.slot and self.name.lower() == other.name.lower() and \
               len(self.attributes) == len(other.attributes) and all(i in other.attributes for i in self.attributes)


def encode_item(item):
    if isinstance(item, Item):
        return {'Name': item.name, 'Slot': item.slot, 'Attributes': {i.type: i.value for i in item.attributes}}
    else:
        type_name = item.__class__.__name__
        raise TypeError(f"Object of type '{type_name}' is not JSON serializable")


def decode_item(json_item):
    name = json_item['Name']
    slot = json_item['Slot']
    attributes = [Attribute(t, v) for t, v in json_item['Attributes'].items()]

    return Item(name, slot, attributes)
