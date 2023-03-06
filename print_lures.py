#!/bin/python
import argparse
from game_data_repository import GameDataRepository
from lure import LurePrintSpecification


parser = argparse.ArgumentParser()
parser.add_argument("lure_id", type=int, nargs="?")
parser.add_argument("--recipe", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--known", action=argparse.BooleanOptionalAction, default=True)

if __name__ == "__main__":
    args = parser.parse_args()
    spec = LurePrintSpecification(
        print_recipe=args.recipe,
        print_known_data=args.known,
    )
    gamedata = GameDataRepository.init().all()
    if args.lure_id is None:
        lures_to_print = gamedata.lures.values()
    else:
        lures_to_print = [gamedata.lures[args.lure_id]]

    [l.print_data(gamedata.items, spec) for l in lures_to_print]
