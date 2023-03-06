import string
import struct
import pydantic

def filter_printable_characters(st):
    return "".join(s for s in st if s in string.printable)

@pydantic.dataclasses.dataclass(frozen=True)
class Item:
    name: str
    description: str
    ID: int
    padding02: bytes

    @staticmethod
    def from_bytes(rd: bytes) -> "Item":
        [name, description, ID, padding02] = struct.unpack("<64s256sH6s", rd)
        return Item(
            name=filter_printable_characters(name.decode("latin-1")),
            description=filter_printable_characters(description.decode("latin-1")),
            ID=ID,
            padding02=padding02,
        )

    def print_data(self):
        print(self.ID, " ", self.name)
