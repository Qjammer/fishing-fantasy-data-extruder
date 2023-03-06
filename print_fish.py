#!/bin/python
import argparse
from fish import FishPrintSpecification
from game_data_repository import GameDataRepository


parser = argparse.ArgumentParser()
parser.add_argument("fish_id", type=int, nargs="?")
parser.add_argument("--useful", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--known", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--unknowns", action=argparse.BooleanOptionalAction, default=False)

if __name__ == "__main__":
    args = parser.parse_args()
    spec = FishPrintSpecification(
        print_useful_data=args.useful,
        print_known_data=args.known,
        print_unknowns=args.unknowns,
    )
    gamedata = GameDataRepository.init().all()
    if args.fish_id is None:
        fishes_to_print = gamedata.fishes.values()
    else:
        fishes_to_print = [gamedata.fishes[args.fish_id]]

    [f.print_data(gamedata.lures, gamedata.items, gamedata.slots, spec) for f in fishes_to_print]
