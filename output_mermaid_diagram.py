#!/bin/python
import string
import numpy as np
from fish_repository import FishRepository
from lure_repository import LureRepository
from item_repository import ItemRepository

fishes = FishRepository().all_indexed()
lures = LureRepository().all_indexed()
items = ItemRepository().all_indexed()

print("graph BT")
for f in fishes.values():
    f.check_lures(lures)
    fish_id = f"fish_{f.ID}"
    fish_name = f.description.name
    print(f"\t{fish_id}(({fish_name}))")

    lure_dep = [f"lure_{l[0]}" for l in f.compatLures if l[1][1] == [0, 0, 0, 0]]
    if lure_dep:
        lure_dep_s = " & ".join(lure_dep)
        print(f"\t{fish_id} --> {lure_dep_s}")
    if f.recipe_drops:
        recipe_dep = " & ".join([f"lure_{l}" for l in f.recipe_drops])
        print(f"\t{recipe_dep} --> {fish_id}")
    if f.item_drops:
        item_dep = " & ".join([f"item_{i}" for i in f.item_drops])
        print(f"\t{item_dep} --> {fish_id}")

for l in lures.values():
    lure_id = f"lure_{l.ID}"
    lure_name = l.name
    print(f"\t{lure_id}{{{{{lure_name}}}}}")

    item_dep = " & ".join([f"item_{i}" for i, b in l.recipe.ingredients])
    print(f"\t{lure_id} --> {item_dep}")

for i in items.values():
    item_id = f"item_{i.ID}"
    item_name = i.name
    print(f"\t{item_id}[{item_name}]")

# (ID, name, crates, complete_deps, complete_rewards)
level_deps: list[tuple[str, str, list[str], list[str], list[str]]] = [
    ("level_1", "Level 1", [], ["fish_0"], ["lure_1", "level_2"]),
    ("level_2", "Level 2", [], ["fish_1"], ["level_3"]),
    ("level_3", "The Dish Pond", [], ["fish_6"], ["item_38", "level_4"]),
    (
        "level_4",
        "The Missing Jungle",
        ["item_34", "item_51", "lure_9", "item_50"],
        ["fish_1"],
        ["item_39", "level_5"],
    ),
    (
        "level_5",
        "The Bush River",
        ["item_23", "item_47"],
        ["fish_2", "fish_8"],
        ["item_40", "level_6"],
    ),
    (
        "level_6",
        "The Haunted Cave",
        ["lure_16", "item_4", "item_5"],
        ["fish_16"],
        ["item_38", "level_7"],
    ),
    (
        "level_7",
        "The Pocket Sea",
        ["item_11", "item_51", "lure_22", "item_15", "item_6"],
        ["fish_22", "fish_24", "fish_25"],
        ["item_39", "level_8"],
    ),
    (
        "level_8",
        "The Big Tree",
        ["item_10", "item_11", "item_32", "item_7"],
        ["fish_30"],
        ["level_9"],
    ),
    ("level_9", "The Last Jungle", ["item_44"], ["fish_33"], [*[f"level_{n}_ngp" for n in range(3,9+1)]]),
    ("level_3_ngp", "The Dish Pond NG+", [], ["fish_7"], []),
    ("level_4_ngp", "The Missing Jungle NG+", [], ["fish_12"], []),
    ("level_5_ngp", "The Bush River NG+", [], ["fish_15"], []),
    ("level_6_ngp", "The Haunted Cave NG+", [], [], []),
    ("level_7_ngp", "The Pocket Sea NG+", [], [], []),
    ("level_8_ngp", "The Big Tree NG+", [], ["fish_31"], []),
    ("level_9_ngp", "The Last Jungle NG+", [], [], []),
]

for level in level_deps:
    level_id = level[0]
    print(f"\tsubgraph {level_id}_sg")
    print(f"\t\t{level_id}{{{level[1]} Unlocked}}")
    print(f"\t\t{level_id}_completed{{{level[1]} Completed}}")
    print(f"\tend")

    # Crates available when level is unlocked
    crates = level[2]
    if crates:
        crates_deps = " & ".join(crates)
        print(f"\t{crates_deps} --> {level_id}")
    # Level completion
    print(f"\t{level_id}_completed --> {level_id}")
    # Dependencies required to complete this level
    complete_deps = level[3]
    if complete_deps:
        complete_deps_s = " & ".join(complete_deps)
        print(f"\t{level_id}_completed -.-> {complete_deps_s}")
    # Rewards obtained when completing this level
    complete_rewards = level[4]
    if complete_rewards:
        complete_rewards_s = " & ".join(complete_rewards)
        print(f"\t{complete_rewards_s} -.-> {level_id}_completed")
