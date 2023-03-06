import enum
import string, struct, binascii
import sys
from typing import Generic, TypeVar
import numpy as np
import pydantic
from lure import Lure
from item import Item
from slot import Slot


def filter_printable_characters(st):
    return "".join(s for s in st if s in string.printable)


class StructuredList:
    @staticmethod
    def from_bytes(rd: bytes, type: str = "H", endianness: str = ">") -> list[int]:
        [item_count, padding] = struct.unpack_from("<H2s", rd)
        values = rd[4:]
        int_list = [v[0] for v in list(struct.iter_unpack(endianness + type, values))]
        sliced = int_list[0:item_count]
        return sliced


@pydantic.dataclasses.dataclass(frozen=True, eq=True)
class FishLurePreferences:
    light: int
    smell: int
    sound: int
    motion: int

    @staticmethod
    def from_bytes(rd: bytes) -> "FishLurePreferences":
        [motion, sound, smell, light] = struct.unpack("<4h", rd)
        return FishLurePreferences(
            light=light,
            smell=smell,
            sound=sound,
            motion=motion,
        )

    def as_array(self) -> list[int]:
        return [self.motion, self.sound, self.smell, self.light]

    def hearts(self, lure: Lure) -> tuple[int, list[int]]:
        dist = 0
        mods = []
        for i in range(4):
            mods.append(0)
            if self.as_array()[i] == -1:
                continue
            tdist = self.as_array()[i] - lure.props.as_list()[i]
            sign = np.sign(tdist)
            adist = abs(tdist)
            if adist < 3:
                mods[i] = 0
            elif adist < 8:
                mods[i] = sign * 5
            elif adist < 16:
                mods[i] = sign * 10
            elif adist < 26:
                mods[i] = sign * 20

            dist += abs(tdist - mods[i])
        if np.count_nonzero(mods) > lure.slots:
            mods = [0, 0, 0, 0]
            dist = 5
        return (max(5 - dist, 0), mods)


T = TypeVar("T")


@pydantic.dataclasses.dataclass(frozen=True, eq=True)
class Range(Generic[T]):
    min: T
    max: T


@pydantic.dataclasses.dataclass(frozen=True, eq=True)
class QuickTimeAllowance:
    # Quicktime event success reeling allowance
    success: int
    # Quicktime event failure reeling allowance
    failure: int


# Swimming direction preference(1=best when reeling up. 0=no preference. -1=best when reeling down... It also probably has to do with whether the fish like the surface and bottom)
class SwimmingDirectionPreference(enum.Enum):
    prefer_up = 1
    no_preference = 0
    prefer_down = -1


@pydantic.dataclasses.dataclass(frozen=True, eq=True)
class FishDescription:
    name: str
    description: str
    clue1: str
    clue2: str
    droptxt: str


@pydantic.dataclasses.dataclass(frozen=True, eq=True)
class FishPrintSpecification:
    print_useful_data: bool
    print_known_data: bool
    print_unknowns: bool


@pydantic.dataclasses.dataclass
class Fish:
    ID: int
    # Description
    description: FishDescription

    # Swimming-phase properties
    scale_range: Range[float]
    swimming_speed_range: Range[float]

    # Luring-phase properties
    best_lures: list[int]
    lure_preferences: FishLurePreferences
    ideal_reeling_speed: int
    lure_swimming_direction_preference: SwimmingDirectionPreference

    # Reeling-phase properties
    quicktime_reeling_allowance: QuickTimeAllowance
    quicktime_duration: int  # Quicktime duration (baseline=100)
    fight_animation_speed: float
    baseline_tension: float
    initial_shakedown_pull: float

    # Reward-phase properties
    weight_range: Range[float]  # Weight in hectograms
    slot_drops: list[int]
    item_drops: list[int]
    recipe_drops: list[int]

    # Other
    constants: dict[int, bytes]
    unknown_floats: dict[int, float]
    unknown_ints: dict[int, int]
    unknowns: dict[int, bytes]
    paddings: dict[int, bytes]

    compatLures: list[tuple[int, tuple[int, list[int]]]] = pydantic.Field(
        default_factory=list
    )

    @staticmethod
    def from_bytes(rd: bytes) -> "Fish":
        [
            name,
            description,
            clue1,
            clue2,
            droptxt,
            ID,
            unknown02,
            padding04,
            float08,
            float12,
            scale_min,
            scale_max,
            weight_min,
            weight_max,
            swimming_speed_min,
            swimming_speed_max,
            padding40,
            int52,
            int54,
            int56,
            swimming_direction_preference,
            quicktime_success_reeling_allowance,
            quicktime_failure_reeling_allowance,
            int64,
            int66,
            quicktime_duration,
            padding70,
            fight_animation_speed,
            float76,
            baseline_tension,
            const84,
            ideal_reeling_speed,
            lure_preferences,
            const98,
            initial_shakedown_pull,
            float104,
            effective_lures,
            recipe_drops,
            item_drops,
            slot_drops,
            padding152,
        ]: tuple[bytes,bytes] = struct.unpack(
            "<64s256s256s256s256sH2s4sffffffff12shhhhhhhhh2sfff4sh8s2sff8s12s12s12s4s",
            rd,
        )
        unknown_floats = {
            8: float08,  # Range of lure detection?
            12: float12,  # Range of lure detection?
            76: float76,  # Reel tension jitter ?
            104: float104,  # Quicktime and pull agressiveness?
        }
        constants = {
            84: const84,  # 10 00 FF 00 (Two constant ints?)
            98: const98,  # 04 00 (bitset?)
        }
        unknown_ints = {
            52: int52,
            54: int54,
            56: int56,
            64: int64,
            66: int66,
        }
        full_unknowns = {
            2: unknown02,  # Some kind of bitset / bool values
        }
        paddings = {
            4: padding04,
            40: padding40,
            70: padding70,
            152: padding152,
        }
        description = FishDescription(
            name=filter_printable_characters(name.decode("latin-1")),
            description=filter_printable_characters(description.decode("latin-1")),
            clue1=filter_printable_characters(clue1.decode("latin-1")),
            clue2=filter_printable_characters(clue2.decode("latin-1")),
            droptxt=filter_printable_characters(droptxt.decode("latin-1")),
        )
        return Fish(
            ID=ID,
            description=description,
            scale_range=Range[float](min=scale_min, max=scale_max),
            swimming_speed_range=Range[float](
                min=swimming_speed_min, max=swimming_speed_max
            ),
            best_lures=StructuredList.from_bytes(effective_lures, "B"),
            lure_preferences=FishLurePreferences.from_bytes(lure_preferences),
            ideal_reeling_speed=ideal_reeling_speed,
            lure_swimming_direction_preference=SwimmingDirectionPreference(
                value=swimming_direction_preference
            ),
            quicktime_reeling_allowance=QuickTimeAllowance(
                success=quicktime_success_reeling_allowance,
                failure=quicktime_failure_reeling_allowance,
            ),
            quicktime_duration=quicktime_duration,
            fight_animation_speed=fight_animation_speed,
            baseline_tension=baseline_tension,
            initial_shakedown_pull=initial_shakedown_pull,
            weight_range=Range[float](min=weight_min, max=weight_max),
            slot_drops=StructuredList.from_bytes(slot_drops),
            item_drops=StructuredList.from_bytes(item_drops),
            recipe_drops=StructuredList.from_bytes(recipe_drops),
            constants=constants,
            unknown_floats=unknown_floats,
            unknown_ints=unknown_ints,
            unknowns=full_unknowns,
            paddings=paddings,
        )

    @pydantic.validator("paddings")
    def validate_padding(cls, paddings: dict[int, bytes]):
        for pos, p in paddings.items():
            for c in p:
                if c != 0:
                    raise ValueError(f"Padding is not zero at position {pos}: {p!r}")

    def lure_hearts(self, lure: Lure) -> tuple[int, list[int]]:
        return self.lure_preferences.hearts(lure)

    def check_lures(self, lures: dict[int, Lure]):
        for ID, lure in lures.items():
            (h, m) = self.lure_hearts(lure)
            if h > 0:
                self.compatLures.append((ID, (h, m)))

    def __print_id(self):
        print(filter_printable_characters(self.description.name), f"({self.ID}):")

    def __print_useful_data(
        self,
        lures: dict[int, Lure],
        items: dict[int, Item],
        slots: dict[int, Slot],
    ):
        print("\t## USEFUL DATA ##")

        print("\tBest Lures", end=": ")
        for l in self.compatLures:
            if np.count_nonzero(l[1][1]) == 0:
                print(filter_printable_characters(lures[l[0]].name), end=" ")
                print("♥" * l[1][0], end=", ")

        print()

        print("\tRecipe Drops", end=": ")
        for i in self.recipe_drops:
            print(filter_printable_characters(lures[i].name), end=", ")
        print()

        print("\tItem Drops", end=": ")
        for i in self.item_drops:
            print(filter_printable_characters(items[i].name), end=", ")
        print()

        print("\tSlot Drops", end=": ")
        for i in self.slot_drops:
            print(filter_printable_characters(slots[i].name), end=", ")
        print()

    def __print_known_data(
        self,
        lures: dict[int, Lure],
        items: dict[int, Item],
        slots: dict[int, Slot],
    ):
        ifmt = "{0}"
        ffmt = "{0:.4f}"
        print("\t## KNOWN DATA ##")
        print(
            "\t3D Model scale range:",
            ffmt.format(self.scale_range.min),
            ffmt.format(self.scale_range.max),
        )
        print(
            "\tWeight range [hg]:",
            ffmt.format(self.weight_range.min),
            ffmt.format(self.weight_range.max),
        )
        print(
            "\tSwimming speed range:",
            ffmt.format(self.swimming_speed_range.min),
            ffmt.format(self.swimming_speed_range.max),
        )
        print(
            "\tSwimming direction preference:",
            ifmt.format(self.lure_swimming_direction_preference.value),
        )
        print(
            "\tQuicktime event success reeling allowance:",
            ifmt.format(self.quicktime_reeling_allowance.success),
        )
        print(
            "\tQuicktime event failure reeling allowance:",
            ifmt.format(self.quicktime_reeling_allowance.failure),
        )
        print("\tQuicktime duration:", ifmt.format(self.quicktime_duration))
        print("\tFight animation speed:", ffmt.format(self.fight_animation_speed))
        print("\tBaseline tension:", ffmt.format(self.baseline_tension))
        print("\tIdeal reeling speed:", ifmt.format(self.ideal_reeling_speed))
        print("\tInitial shakedown pull:", ffmt.format(self.initial_shakedown_pull))

    def __print_unknown_data(self):
        print("\t## UNKNOWN DATA ##")
        for pos, v in self.unknowns.items():
            print(f"\t[{pos}]\t{binascii.hexlify(v)}")
        for pos, v in self.unknown_ints.items():
            print(f"\t[{pos}]\t{v}")
        for pos, f in self.unknown_floats.items():
            print(f"\t[{pos}]\t{f:.4f}")

    def print_data(
        self,
        lures: dict[int, Lure],
        items: dict[int, Item],
        slots: dict[int, Slot],
        spec: FishPrintSpecification,
    ):
        self.check_lures(lures)
        self.__print_id()
        if spec.print_useful_data:
            self.__print_useful_data(lures, items, slots)
            print()
        if spec.print_known_data:
            self.__print_known_data(lures, items, slots)
            print()
        if spec.print_unknowns:
            self.__print_unknown_data()
            print()
