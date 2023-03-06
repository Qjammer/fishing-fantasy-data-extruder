import string, struct
import pydantic
from item import Item


def filter_printable_characters(st):
    return "".join(s for s in st if s in string.printable)


@pydantic.dataclasses.dataclass(frozen=True)
class LureRecipe:
    ingredients: list[int]

    @staticmethod
    def from_bytes(rd: bytes) -> "LureRecipe":
        splitted_str = [rd[n : n + 2] for n in range(0, len(rd), 2)]
        recipe_items = [struct.unpack("<B?", n) for n in splitted_str]
        recipe_items = [r[0] for r in recipe_items if r[1]]
        return LureRecipe(ingredients=recipe_items)

    def print(self, items: dict[int, Item]):
        print("\tRecipe:",[items[id].name for id in self.ingredients])

@pydantic.dataclasses.dataclass(frozen=True)
class LureProperties:
    light: int
    smell: int
    sound: int
    motion: int

    @staticmethod
    def from_bytes(rd: bytes) -> "LureProperties":
        [motion, sound, smell, light] = struct.unpack("<4h", rd)
        return LureProperties(
            light=light,
            smell=smell,
            sound=sound,
            motion=motion,
        )

    def as_list(self) -> list[int]:
        return [self.motion, self.sound, self.smell, self.light]

    def print(self):
        print("\tProperties:", self.as_list())


@pydantic.dataclasses.dataclass(frozen=True)
class LurePrintSpecification:
    print_recipe: bool
    print_known_data: bool

@pydantic.dataclasses.dataclass(frozen=True)
class Lure:
    ID: int
    prefix: bytes
    name: str
    desc: str
    props: LureProperties
    slots: int
    base_sink_speed: float
    reeling_sink_speed: float
    padding01: bytes
    recipe: LureRecipe

    @staticmethod
    def from_bytes(rd: bytes) -> "Lure":
        [
            prefix,
            name,
            desc,
            ID,
            padding01,
            slots,
            float04,
            float08,
            props,
            recipe,
        ] = struct.unpack("<4s64s256sH1sBff8s20s", rd)
        return Lure(
            prefix=prefix,
            name=filter_printable_characters(name.decode("latin-1")),
            desc=filter_printable_characters(desc.decode("latin-1")),
            ID=ID,
            props=LureProperties.from_bytes(props),
            slots=slots,
            base_sink_speed=float04,
            reeling_sink_speed=float08,
            padding01=padding01,
            recipe=LureRecipe.from_bytes(recipe),
        )

    def print_id(self):
        print(filter_printable_characters(self.name), end=" (")
        print(self.ID, end="):\n")

    def print_data(self, items, spec: LurePrintSpecification):
        self.print_id()
        if spec.print_known_data:
            self.print_known_data()
        if spec.print_recipe:
            self.print_recipe(items)

        print()

    def print_known_data(self):
        print("\t## KNOWN DATA ##")

        print("\tNumber of slots: ", self.slots)
        print("\tSink speed: ", "{:.3f}".format(self.base_sink_speed))
        print("\tReel speed: ", "{:.3f}".format(self.reeling_sink_speed))
        self.props.print()
    def print_recipe(self, items):
        self.recipe.print(items)