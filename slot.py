import struct
import pydantic


@pydantic.dataclasses.dataclass(frozen=True)
class SlotPropertyModifiers:
    motion: int
    sound: int
    smell: int
    light: int

    @staticmethod
    def fromBytes(rd: bytes) -> "SlotPropertyModifiers":
        return SlotPropertyModifiers(*struct.unpack("<4H", rd))


@pydantic.dataclasses.dataclass(frozen=True)
class Slot:
    ID: int
    name: str
    description: str
    consumable: bytes
    property_modifiers: SlotPropertyModifiers
    paddings: dict[int, bytes]

    @staticmethod
    def from_bytes(rd: bytes) -> "Slot":
        [
            consumable,
            name,
            desc,
            ID,
            padding02,
            props,
            padding12,
        ] = struct.unpack("<4s64s256sH2s8s4s", rd)
        paddings = {
            2: padding02,
            12: padding12,
        }
        return Slot(
            consumable=consumable,
            name=name.decode("latin-1"),
            description=desc.decode("latin-1"),
            ID=ID,
            property_modifiers=SlotPropertyModifiers.fromBytes(props),
            paddings=paddings,
        )

    def print_data(self):
        print(hex(self.ID), "\t", self.name, "\t", self.description)
