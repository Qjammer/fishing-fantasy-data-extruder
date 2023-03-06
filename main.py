#!/bin/python
from game_data_repository import GameDataRepository
from item import Item
from lure import Lure
from slot import Slot


def printAllLureData(lures: dict[int, Lure]):
    for lure in lures.values():
        lure.print_data()


def printAllItemData(items: dict[int, Item]):
    for item in items.values():
        item.print_data()


def printAllSlotData(slots: dict[int, Slot]):
    for slot in slots.values():
        slot.print_data()


gamedata = GameDataRepository.init().all()
# printAllItemData(items)
# printAllSlotData(slots)
printAllLureData(gamedata.lures)
