#!/bin/python
from collections import defaultdict
from game_data_repository import GameDataRepository


if __name__ == "__main__":
    gamedata = GameDataRepository.init().all()
    fish_by_unknown = defaultdict(list)
    for fish in gamedata.fishes.values():
        unknown = fish.unknown_ints[66]
        fish_by_unknown[unknown].append(fish)
    for k in sorted(fish_by_unknown):
        fishes = fish_by_unknown[k]
        print(f"{k:.4f}")
        for fish in fishes:
            print("\t",fish.description.name)